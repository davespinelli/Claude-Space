-- Monarch discovery (READ-ONLY). Run in SSMS against the Monarch database. Save each result grid as CSV.
SET NOCOUNT ON;
-- 1. Server / database facts
SELECT @@VERSION AS sql_version, DB_NAME() AS database_name, SUSER_SNAME() AS login_name;
-- 2. All tables with row counts
SELECT s.name AS schema_name, t.name AS table_name, SUM(p.rows) AS row_count
FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id
JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name ORDER BY row_count DESC;
-- 3. Columns of tables relevant to estimating, jobs, planning
SELECT c.TABLE_SCHEMA, c.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE, c.CHARACTER_MAXIMUM_LENGTH, c.IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.TABLE_NAME LIKE '%estim%' OR c.TABLE_NAME LIKE '%quote%' OR c.TABLE_NAME LIKE '%standard%'
   OR c.TABLE_NAME LIKE '%rate%' OR c.TABLE_NAME LIKE '%price%' OR c.TABLE_NAME LIKE '%job%'
   OR c.TABLE_NAME LIKE '%plan%' OR c.TABLE_NAME LIKE '%sched%' OR c.TABLE_NAME LIKE '%customer%'
   OR c.TABLE_NAME LIKE '%product%' OR c.TABLE_NAME LIKE '%stock%' OR c.TABLE_NAME LIKE '%paper%'
   OR c.TABLE_NAME LIKE '%press%' OR c.TABLE_NAME LIKE '%operation%' OR c.TABLE_NAME LIKE '%import%'
ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION;
-- 4. Foreign keys among those tables (how estimates link to lines, standards, jobs)
SELECT fk.name AS fk_name, tp.name AS parent_table, cp.name AS parent_column, tr.name AS referenced_table, cr.name AS referenced_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
JOIN sys.tables tp ON tp.object_id = fkc.parent_object_id
JOIN sys.columns cp ON cp.object_id = fkc.parent_object_id AND cp.column_id = fkc.parent_column_id
JOIN sys.tables tr ON tr.object_id = fkc.referenced_object_id
JOIN sys.columns cr ON cr.object_id = fkc.referenced_object_id AND cr.column_id = fkc.referenced_column_id
ORDER BY parent_table;
-- 5. Stored procedures and views that mention import, XML, estimate or job (names only)
SELECT o.type_desc, s.name AS schema_name, o.name AS object_name, o.modify_date
FROM sys.objects o JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE o.type IN ('P','V','FN','IF','TF') AND (o.name LIKE '%import%' OR o.name LIKE '%xml%' OR o.name LIKE '%estim%' OR o.name LIKE '%job%' OR o.name LIKE '%quote%')
ORDER BY o.type_desc, o.name;
-- 6. Recent estimates (adjust the table name after seeing result 3; this guesses common names)
IF OBJECT_ID('dbo.Estimate') IS NOT NULL SELECT TOP 200 * FROM dbo.Estimate ORDER BY 1 DESC;
IF OBJECT_ID('dbo.Estimates') IS NOT NULL SELECT TOP 200 * FROM dbo.Estimates ORDER BY 1 DESC;
IF OBJECT_ID('dbo.EstimateHeader') IS NOT NULL SELECT TOP 200 * FROM dbo.EstimateHeader ORDER BY 1 DESC;
IF OBJECT_ID('dbo.Job') IS NOT NULL SELECT TOP 200 * FROM dbo.Job ORDER BY 1 DESC;
IF OBJECT_ID('dbo.Jobs') IS NOT NULL SELECT TOP 200 * FROM dbo.Jobs ORDER BY 1 DESC;
