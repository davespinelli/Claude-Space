<#  Export-SqlDefinitions.ps1 - READ-ONLY export of a SQL Server database's code and structure. No data rows.

    Nothing to install: it uses Windows PowerShell 5.1 and the .NET SQL client that ship with Windows.
    Run it on any PC that can already reach the database server (for example, a PC where the Monarch client runs).

    Usage:
      powershell -ExecutionPolicy Bypass -File .\Export-SqlDefinitions.ps1 -Server "SERVER\INSTANCE" -Database "Monarch"
      Add -SqlLogin to use a SQL login instead of your Windows login (you type the password; it is not saved).

    Output: Desktop\SqlDefinitions_<db>_<time>\ plus a zip beside it.
      Procedures\, Views\, Functions\, Triggers\   one .sql file per object
      ALL_DEFINITIONS.sql                          every definition in one file
      00_manifest.csv                              every object, and whether its code was readable
      01_server.csv  02_databases.csv  03_tables.csv  04_columns.csv  05_foreign_keys.csv
      06_dependencies.csv (which procedure uses which table)  07_agent_jobs.csv (scheduled jobs, if permitted)

    It only runs SELECT statements against system catalog views. It changes nothing.
    Seeing procedure code needs the VIEW DEFINITION permission. If 00_manifest.csv says "not visible",
    ask IT to run:  GRANT VIEW DEFINITION TO [DOMAIN\your.name];  (read-only, gives no access to data)
    or ask IT to run this script with their own login. #>
param(
  [Parameter(Mandatory=$true)][string]$Server,
  [Parameter(Mandatory=$true)][string]$Database,
  [switch]$SqlLogin
)
$ErrorActionPreference = "Stop"

$stamp = Get-Date -Format "yyyyMMdd_HHmm"
$desk  = [Environment]::GetFolderPath("Desktop")
$safeDb = $Database -replace '[^A-Za-z0-9_-]', '_'
$out   = Join-Path $desk ("SqlDefinitions_{0}_{1}" -f $safeDb, $stamp)
New-Item -ItemType Directory -Force -Path $out | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)

# ---- connect (read-only intent; Windows login unless -SqlLogin) ----
$csb = New-Object System.Data.SqlClient.SqlConnectionStringBuilder
$csb["Data Source"]            = $Server
$csb["Initial Catalog"]        = $Database
$csb["Application Name"]       = "Read-only schema export"
$csb["TrustServerCertificate"] = $true
if ($SqlLogin) {
  $cred = Get-Credential -Message "SQL login for $Server"
  $pw = $cred.Password; $pw.MakeReadOnly()
  $sqlCred = New-Object System.Data.SqlClient.SqlCredential($cred.UserName, $pw)
  $conn = New-Object System.Data.SqlClient.SqlConnection($csb.ConnectionString, $sqlCred)
} else {
  $csb["Integrated Security"] = $true
  $conn = New-Object System.Data.SqlClient.SqlConnection($csb.ConnectionString)
}
$conn.Open()
Write-Host "Connected to $Server / $Database"

function Invoke-Q([string]$sql) {
  $cmd = $conn.CreateCommand()
  $cmd.CommandText = $sql
  $cmd.CommandTimeout = 300
  $da = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
  $dt = New-Object System.Data.DataTable
  [void]$da.Fill($dt)
  return ,$dt
}
function Save-Csv($dt, [string]$name) {
  $dt.Rows | Select-Object -Property ($dt.Columns | ForEach-Object { $_.ColumnName }) |
    Export-Csv -Path (Join-Path $out $name) -NoTypeInformation -Encoding UTF8
}
function Try-Save([string]$name, [string]$sql) {
  try { Save-Csv (Invoke-Q $sql) $name; Write-Host "  $name" }
  catch { Write-Warning ("  skipped {0}: {1}" -f $name, $_.Exception.Message)
          Set-Content -Path (Join-Path $out ($name + ".skipped.txt")) -Value $_.Exception.Message }
}

# ---- permission check ----
$perm = Invoke-Q "SELECT HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'VIEW DEFINITION') AS can_view_definition"
if ($perm.Rows[0].can_view_definition -ne 1) {
  Write-Warning "Your login lacks VIEW DEFINITION: object names will export, but most code will show as 'not visible'."
}

# ---- structure ----
Write-Host "Exporting structure..."
Try-Save "01_server.csv" @"
SELECT @@VERSION AS sql_version, @@SERVERNAME AS server_name, DB_NAME() AS db, SUSER_SNAME() AS login_name,
       (SELECT compatibility_level FROM sys.databases WHERE name = DB_NAME()) AS compatibility_level,
       SYSDATETIME() AS exported_at
"@
Try-Save "02_databases.csv" "SELECT name, create_date, state_desc, compatibility_level FROM sys.databases ORDER BY name"
Try-Save "03_tables.csv" @"
SELECT s.name AS schema_name, t.name AS table_name, SUM(p.rows) AS row_count, t.create_date, t.modify_date
FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id
JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name, t.create_date, t.modify_date ORDER BY row_count DESC
"@
Try-Save "04_columns.csv" @"
SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH,
       NUMERIC_PRECISION, NUMERIC_SCALE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
"@
Try-Save "05_foreign_keys.csv" @"
SELECT fk.name AS fk_name, SCHEMA_NAME(tp.schema_id) AS parent_schema, tp.name AS parent_table, cp.name AS parent_column,
       SCHEMA_NAME(tr.schema_id) AS referenced_schema, tr.name AS referenced_table, cr.name AS referenced_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
JOIN sys.tables tp  ON tp.object_id = fkc.parent_object_id
JOIN sys.columns cp ON cp.object_id = fkc.parent_object_id AND cp.column_id = fkc.parent_column_id
JOIN sys.tables tr  ON tr.object_id = fkc.referenced_object_id
JOIN sys.columns cr ON cr.object_id = fkc.referenced_object_id AND cr.column_id = fkc.referenced_column_id
ORDER BY parent_table, fk_name
"@
Try-Save "06_dependencies.csv" @"
SELECT OBJECT_SCHEMA_NAME(d.referencing_id) AS referencing_schema, OBJECT_NAME(d.referencing_id) AS referencing_object,
       o.type_desc AS referencing_type, d.referenced_database_name, d.referenced_schema_name, d.referenced_entity_name
FROM sys.sql_expression_dependencies d JOIN sys.objects o ON o.object_id = d.referencing_id
ORDER BY referencing_object, d.referenced_entity_name
"@
Try-Save "07_agent_jobs.csv" @"
SELECT j.name AS job_name, j.enabled, j.date_modified, s.step_id, s.step_name, s.subsystem, s.database_name, s.command
FROM msdb.dbo.sysjobs j JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id
ORDER BY j.name, s.step_id
"@

# ---- code: procedures, views, functions, triggers ----
Write-Host "Exporting code..."
$defs = Invoke-Q @"
SELECT s.name AS schema_name, o.name AS object_name, o.type, o.type_desc, o.create_date, o.modify_date,
       CAST(ISNULL(OBJECTPROPERTY(o.object_id, 'IsEncrypted'), 0) AS int) AS is_encrypted,
       m.definition
FROM sys.objects o
JOIN sys.schemas s ON s.schema_id = o.schema_id
LEFT JOIN sys.sql_modules m ON m.object_id = o.object_id
WHERE o.type IN ('P','V','FN','IF','TF','TR','PC','FS','FT') AND o.is_ms_shipped = 0
ORDER BY o.type, s.name, o.name
"@
$folders = @{ 'P'='Procedures'; 'PC'='Procedures'; 'V'='Views'; 'FN'='Functions'; 'IF'='Functions'; 'TF'='Functions'; 'FS'='Functions'; 'FT'='Functions'; 'TR'='Triggers' }
$all = New-Object System.Text.StringBuilder
$manifest = New-Object System.Collections.Generic.List[object]
foreach ($r in $defs.Rows) {
  $type = ([string]$r.type).Trim()
  $name = "{0}.{1}" -f $r.schema_name, $r.object_name
  $def  = if ($r.definition -is [DBNull]) { $null } else { [string]$r.definition }
  if ($def) { $status = "exported" }
  elseif ($r.is_encrypted -eq 1) { $status = "encrypted by vendor" }
  elseif ($type -in @('PC','FS','FT')) { $status = "compiled .NET code (no SQL text)" }
  else { $status = "not visible (needs VIEW DEFINITION)" }
  $file = ""
  if ($def) {
    $dir = Join-Path $out $folders[$type]
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $fname = ($name -replace '[\\/:*?"<>|]', '_') + ".sql"
    $file = Join-Path $folders[$type] $fname
    [System.IO.File]::WriteAllText((Join-Path $out $file), $def, $utf8)
    [void]$all.AppendLine(("-- ===== {0} {1}  (modified {2:yyyy-MM-dd})" -f $r.type_desc, $name, $r.modify_date))
    [void]$all.AppendLine($def)
    [void]$all.AppendLine("GO")
    [void]$all.AppendLine("")
  }
  $manifest.Add([pscustomobject]@{
    schema_name = $r.schema_name; object_name = $r.object_name; type = $r.type_desc
    created = $r.create_date; modified = $r.modify_date
    chars = if ($def) { $def.Length } else { 0 }; status = $status; file = $file })
}
[System.IO.File]::WriteAllText((Join-Path $out "ALL_DEFINITIONS.sql"), $all.ToString(), $utf8)
$manifest | Export-Csv -Path (Join-Path $out "00_manifest.csv") -NoTypeInformation -Encoding UTF8
$conn.Close()

# ---- summary + zip ----
Write-Host ""
Write-Host "Objects found: $($manifest.Count)"
$manifest | Group-Object status | ForEach-Object { Write-Host ("  {0,-40} {1}" -f $_.Name, $_.Count) }
$zip = "$out.zip"
Compress-Archive -Path (Join-Path $out "*") -DestinationPath $zip -Force
Write-Host ""
Write-Host "Done. Bring this one file to the Mac (Claude Space/products/anro/):"
Write-Host "  $zip"
