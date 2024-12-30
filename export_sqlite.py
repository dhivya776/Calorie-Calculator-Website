import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Dump the schema and data
with open('sqlite_dump.sql', 'w') as f:
    for line in conn.iterdump():
        f.write(f'{line}\n')

# Close the connection
conn.close()

print("SQLite dump complete")
