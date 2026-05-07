/*
Run this manually in SQL Server Management Studio or another SQL Server client.
The database name contains hyphens, so it is quoted with square brackets.
*/

IF DB_ID(N'ezeas-intelligence-db') IS NULL
BEGIN
    CREATE DATABASE [ezeas-intelligence-db];
END;
GO
