# Yaml defined database migration tool.

This program uses a yaml file (mapping.yaml) to define the migration specifications from an SQL Server database to a PostgreSQL database.

To utilize the tool complete the following steps:

1. Define connection specifications for the source database.
2. Define connection specifications for the traaget database.
3. Under the tables section of mapping.yaml, first define a name for the migration (ie. Users, Companies).
4. define the source table, and the target table.
5. Under columns, define the specific source, and target column which the data waill migrate from and to.
6. For each column, define the datatype the receiving database is expecting.

## Transforms:
If a transform is necessary to transform the data from the source database to the target database, a transform key can be added for each column. Right now only "upper" and "date_only" transforms are implemented.

## Done key:
A done key can be added for each individual migration (ie. Users, Companies). When set to false, the migration will be run on every run of main.py. If set to false it will be skipped. The done key can also 
be used for each individual column. This should help reduce repeat migrations, should additional data be necessary.

## ODBC Driver for SQL Server Connections
An ODBC Driver may be necessary to complete the database connection. It can be found here:

https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17
