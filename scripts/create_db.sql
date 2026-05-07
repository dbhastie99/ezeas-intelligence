/*
Minerva local SQL Server database bootstrap.

Run this manually in SQL Server Management Studio, Azure Data Studio, or sqlcmd.
It creates the local Minerva database only if it does not already exist.

The database name contains hyphens, so it is quoted with square brackets.
The operational payroll database is separate and must not be used for Minerva.
*/

IF DB_ID(N'ezeas-intelligence-db') IS NULL
BEGIN
    CREATE DATABASE [ezeas-intelligence-db];
END;
GO
