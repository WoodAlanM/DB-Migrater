import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from datetime import datetime
from tqdm import tqdm
import time
import urllib.parse


# Load mapping configuration
with open("mapping.yaml") as file:
    config = yaml.safe_load(file)


# Use source and target database configurations to make connection URL's
def make_url(cfg):
    if cfg["type"] == "sqlserver":
        encrypt = "yes" if cfg.get("encrypt", False) else "no"
        connection_url = URL.create(
            "mssql+pyodbc",
            username=cfg["username"],
            password=cfg["password"],
            host=cfg["host"],
            port=cfg["port"],
            database=cfg["database"],
            query={
                "driver": cfg["driver"],
                "TrustServerCertificate": cfg["trust-server-certificate"],
                "encrypt": cfg["encrypt"],
            }
        )
        return connection_url
    elif cfg["type"] == "postgres":
        return (
            f"postgresql://{cfg['username']}:{cfg['password']}@"
            f"{cfg['host']}:{cfg['port']}/{cfg['database']}"
        )
    return None

# Make connections using source and target data
source_engine = create_engine(make_url(config["source"]))
print(f"Connected to {source_engine.url}")
target_engine = create_engine(make_url(config["target"]))
print(f"Connected to {target_engine.url}")


def transform_value(value, transform):
    if transform == "upper":
        return value.upper() if value else None
    elif transform == "date_only":
        return value.date() if value else None
    return value


# Perform migration
for table, mapping in config["tables"].items():
    # Skip whole table if done
    if mapping.get("done", False):
        print(f"Skipping {table} (marked done)")
        continue

    # Only include active columns
    active_columns = [c for c in mapping["columns"] if not c.get("done", False)]
    if not active_columns:
        print(f"Skipping {table} (no active columns)")
        continue

    # Start per-table timer
    table_start = time.time()

    with source_engine.connect() as src, target_engine.begin() as tgt:
        # Build SELECT only with active columns
        query = f"SELECT {','.join(c['source'] for c in active_columns)} FROM {mapping['source']}"
        rows = src.execute(text(query)).fetchall()

        # Wrap row iteration with tqdm
        for row in tqdm(rows, desc=f"Migrating {table}", unit="row"):
            values = []
            for i, col in enumerate(active_columns):
                val = row[i]
                val = transform_value(val, col.get("transform"))
                values.append(val)

            placeholders = ",".join([f":v{i}" for i in range(len(values))])
            target_cols = ",".join(c["target"] for c in active_columns)
            insert_sql = text(
                f"INSERT INTO {mapping['target']} ({target_cols}) VALUES ({placeholders})"
            )
            params = {f"v{i}": values[i] for i in range(len(values))}
            tgt.execute(insert_sql, params)

    elapsed = time.time() - table_start
    print(f"Finished {table} in {elapsed:.2f} seconds\n")
