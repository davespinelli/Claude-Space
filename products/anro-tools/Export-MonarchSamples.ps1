<#  Export-MonarchSamples.ps1  —  READ-ONLY discovery export of a Monarch SQL Server database.
    Usage:  .\Export-MonarchSamples.ps1 -Server "SERVER\INSTANCE" -Database "Monarch"
    Uses your Windows login. Writes Desktop\MonarchDiscovery\*.csv and a zip. Changes nothing in the database. #>
param([Parameter(Mandatory=$true)][string]$Server, [Parameter(Mandatory=$true)][string]$Database, [int]$Top = 200)
$ErrorActionPreference = "Stop"
$out = Join-Path ([Environment]::GetFolderPath("Desktop")) "MonarchDiscovery"; New-Item -ItemType Directory -Force -Path $out | Out-Null
if (-not (Get-Module -ListAvailable -Name SqlServer)) { Write-Host "Installing SqlServer PowerShell module (user scope)…"; Install-Module SqlServer -Scope CurrentUser -Force -AllowClobber }
Import-Module SqlServer
function Q($sql) { Invoke-Sqlcmd -ServerInstance $Server -Database $Database -Query $sql -TrustServerCertificate -QueryTimeout 120 }
Write-Host "Connected to $Server / $Database as $env:USERNAME"
Q "SELECT @@VERSION AS sql_version, DB_NAME() AS db, SUSER_SNAME() AS login_name" | Export-Csv "$out\00_server.csv" -NoTypeInformation
Q @"
SELECT s.name AS schema_name, t.name AS table_name, SUM(p.rows) AS row_count
FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.partitions p ON p.object_id=t.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name ORDER BY row_count DESC
"@ | Export-Csv "$out\01_tables.csv" -NoTypeInformation
Q "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, ORDINAL_POSITION FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME, ORDINAL_POSITION" | Export-Csv "$out\02_columns.csv" -NoTypeInformation
Q @"
SELECT fk.name AS fk_name, tp.name AS parent_table, cp.name AS parent_column, tr.name AS referenced_table, cr.name AS referenced_column
FROM sys.foreign_keys fk JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id=fk.object_id
JOIN sys.tables tp ON tp.object_id=fkc.parent_object_id JOIN sys.columns cp ON cp.object_id=fkc.parent_object_id AND cp.column_id=fkc.parent_column_id
JOIN sys.tables tr ON tr.object_id=fkc.referenced_object_id JOIN sys.columns cr ON cr.object_id=fkc.referenced_object_id AND cr.column_id=fkc.referenced_column_id
"@ | Export-Csv "$out\03_foreign_keys.csv" -NoTypeInformation
Q "SELECT o.type_desc, s.name AS schema_name, o.name AS object_name, o.modify_date FROM sys.objects o JOIN sys.schemas s ON s.schema_id=o.schema_id WHERE o.type IN ('P','V','FN','IF','TF') ORDER BY o.type_desc, o.name" | Export-Csv "$out\04_procs_views.csv" -NoTypeInformation
$patterns = "estim","quote","standard","rate","price","job","plan","sched","customer","product","stock","paper","press","operation","import","cost","ink","finish","bindery","depart"
$tables = Q "SELECT s.name AS sch, t.name AS tbl FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id"
$picked = $tables | Where-Object { $n = $_.tbl.ToLower(); ($patterns | Where-Object { $n -like "*$_*" }).Count -gt 0 }
Write-Host ("Sampling {0} tables (TOP {1} rows each)…" -f $picked.Count, $Top)
foreach ($t in $picked) {
  try { Q ("SELECT TOP {0} * FROM [{1}].[{2}]" -f $Top, $t.sch, $t.tbl) | Export-Csv ("$out\sample_{0}.csv" -f $t.tbl) -NoTypeInformation }
  catch { Write-Warning ("skip {0}: {1}" -f $t.tbl, $_.Exception.Message) }
}
$zip = Join-Path ([Environment]::GetFolderPath("Desktop")) ("MonarchDiscovery_{0}.zip" -f (Get-Date -Format yyyyMMdd_HHmm))
Compress-Archive -Path "$out\*" -DestinationPath $zip -Force
Write-Host "Done. Bring this file to the Mac -> Claude Space/products/anro/ :`n$zip"
