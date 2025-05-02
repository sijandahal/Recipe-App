import pandas as pd
from sqlalchemy import create_engine
import os

# Connection
engine = create_engine("mysql+mysqlconnector://root:root@mysql:3306/forkast")

# Output file path
csv_path = "/app/recipes.csv"
chunksize = 100000
first_chunk = True

# Delete existing CSV if any
if os.path.exists(csv_path):
    os.remove(csv_path)

# Read in chunks and write
for chunk in pd.read_sql("SELECT * FROM recipes", engine, chunksize=chunksize):
    print(f"📦 Writing chunk with {len(chunk)} rows")
    chunk.to_csv(csv_path, mode='a', index=False, header=first_chunk)
    first_chunk = False

print("✅ Done exporting to CSV at", csv_path)
