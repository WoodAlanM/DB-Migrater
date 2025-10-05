# Yaml defined database migration tool.

This program uses a yaml file (mapping.yaml) to define the migration specifications from an SQL Server database to a PostgreSQL database.

To utilize the tool complete the following steps:

1. Define connection specifications for the source database.
```yaml
  source:
    type: sqlserver
    host: <SQL Server hostname>
    port: <Port assigned to SQL Server Instance>
    database: <Database name>
    username: "sa" # Username for accesing db. The sa username is the default user
    password: "Mysecurepassword"
    driver: "ODBC Driver 18 for SQL Server" # If this driver is not available a link to it can be found below
    encrypt: "yes"
    trust-server-certificate: "Yes"
```
2. Define connection specifications for the traaget database.
```yaml
  target:
    type: postgres
    host: "192.168.x.x" # IP of postgres db server
    port: 5433 # Port number for postgres db server
    database: <Database name>
    username: "username"
    password: "password"
```  
3. Under the tables section of mapping.yaml, first define a name for the migration (ie. Users, Companies).
```yaml
tables:
  users: # This is the name of a group of migrationse. This can be disabled for future migrations
```
4. define the source table, and the target table.
```yaml
  users:
    source: "dbo.tab_User" # Source database table
    target: "users"        # Target database table
```
5. Under columns, define the specific source, and target column which the data waill migrate from and to.
```yaml
    columns:
      - source: "User_GUID" # Table column from
        target: "id"        # Table column to
```
6. For each column, define the datatype the receiving database is expecting.
```yaml
    columns:
      - source: "User_GUID"
        target: "id"
        type: "str" # The target database expects a string value
```

## Transforms:
If a transform is necessary to transform the data from the source database to the target database, a transform key can be added for each column. Right now only "upper" and "date_only" transforms are implemented.

```yaml
    columns:
      - source: "User_GUID"
        target: "id"
        type: "str"
        done: false
      - source: "User_NameFirst"
        target: "first_name"
        type: "str"
        transform: "upper" # Will store "User_NameFirst" into "first_name" in upper case format.
        done: false
```

## Done key:
A done key can be added for each individual migration (ie. Users, Companies). When set to false, the migration will be run on every run of main.py. If set to false it will be skipped. The done key can also 
be used for each individual column. This should help reduce repeat migrations, should additional data be necessary.

```yaml
tables:
  users:
    source: "dbo.tab_User"
    target: "users"
    done: false # The users migration will be run
    columns:
      - source: "User_GUID"
        target: "id"
        type: "str"
        done: true # The "User_GUID" to "id" migration will not run
      - source: "User_NameFirst"
        target: "first_name"
        type: "str"
        done: false
```

## ODBC Driver for SQL Server Connections
An ODBC Driver may be necessary to complete the database connection. It can be found here:

https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17
