import os
import duckdb

# Setar o db_path
db_path = 'duckdb/salic.db'

# Cria o diretório se ele não existir
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create parameters
params = {
    'database': db_path
}

# Connect to DuckDB with the parameters
conn = duckdb.connect(**params)

