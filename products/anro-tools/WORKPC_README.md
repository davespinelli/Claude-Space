# Monarch discovery — steps for the work PC (read-only, nothing is changed)

Goal: give Claude enough to learn how ANRO's Monarch Foundation estimates and the existing XML importer are structured. Everything below reads; nothing writes. Do not put any exported company data on GitHub; bring it to the Mac and drop it in `Claude Space/products/anro/` (that folder is excluded from the repo).

## A. Three quick facts (5 minutes)
1. **Monarch version:** open the Monarch client → Help → About. Photograph or note the version (e.g. 13.x).
2. **SQL Server name and database name:** in the Monarch client login or config, or ask IT: "What is the SQL Server instance and database name for Monarch?" (looks like `SERVER\INSTANCE` and `Monarch` or `MonarchDB`).
3. **The XMPie → Monarch importer:** ask whoever maintains it: (a) where does it drop the XML files (folder path), (b) what does it call to import (Monarch XML import service, Integration Services, a stored procedure), (c) can I have TWO sample XML files it produced (one subjob import, one anything else). Copy those files to a USB/AirDrop → `products/anro/xml_samples/`.

## B. Database discovery export (15 minutes, read-only)
Option 1 (easiest if you have SQL Server Management Studio):
1. Open SSMS, connect to the Monarch server (Windows authentication is usually enough for read).
2. Open `monarch_discovery.sql` from this folder, select the Monarch database in the dropdown, press F5.
3. Right-click each result grid → "Save Results As…" → CSV into a folder `MonarchDiscovery` on your Desktop.

Option 2 (PowerShell, exports everything to CSV automatically):
1. Download `Export-MonarchSamples.ps1` (Raw file from GitHub) to your Desktop.
2. Right-click PowerShell → Run as yourself (no admin needed). If scripts are blocked: `Set-ExecutionPolicy -Scope Process Bypass`.
3. Run: `.\Export-MonarchSamples.ps1 -Server "SERVER\INSTANCE" -Database "Monarch"`
   It prompts nothing else; uses your Windows login; writes `Desktop\MonarchDiscovery\*.csv` and zips it.
4. Bring the zip to the Mac → `Claude Space/products/anro/`.

What the scripts collect: table and column catalogue; row counts; the first 200 rows of every table whose name contains estimate, quote, standard, rate, price, job, subjob, plan, schedule, customer, product, stock, press, or operation. No personal data beyond what is in those business tables; if a table holds payroll or HR data, delete that CSV before bringing it over.

## C. If IT asks what this is for
"Read-only export of estimating structures so we can build an estimate-preparation assistant that drafts estimates for an estimator to review. No writes to Monarch, no vendor API yet."
