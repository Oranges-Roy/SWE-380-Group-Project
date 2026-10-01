from posixpath import basename
import sqlite3
import pandas as pd
import os
# Define default database path
default_dbpath = "agent_skills_release.db"
# Loop until a valid database file path is provided
while True:
    user_input = (
        input(f"Enter path to agent_skills_release.db (copy as path) (press Enter for default '{default_dbpath}'): ")
        .strip()
        .strip("'\"")
    )
    # Use default if user hits Enter without typing a path
    dbpath = user_input if user_input else default_dbpath
    # Verify file existence
    if os.path.isfile(dbpath):
        print(f"Connecting to database at: {dbpath}")
        break
    else:
        print(f"Error: File '{dbpath}' not found. Please enter a valid path.\n")
conn = sqlite3.connect(dbpath)
# Query filtering by C++ and joining repos with artifacts
query = """
SELECT 
    a.repo_full_name,
    a.path,
    a.filename,
    a.name,
    a.file_sha,
    a.content,
    a.dedup_primary,
    r.language,
    r.stars
FROM artifacts a
JOIN repos r ON a.repo_full_name = r.full_name
WHERE LOWER(r.language) IN ('c++', 'cpp');
"""
df = pd.read_sql_query(query, conn)
conn.close()
# Save sample output
print(f"Total skills extracted: {len(df)}")
# Create the 'results' directory if it doesn't exist
os.makedirs("results", exist_ok=True)
# Save output
df.to_csv("results/extracted_skills_sample.csv", index=False)