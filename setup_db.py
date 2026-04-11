import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT  NOT NULL,password TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, severity TEXT, description TEXT, user TEXT, date TEXT)""")

conn.commit()
conn.close()

print("Database created successfully")

conn = sqlite3.connect("database.db")

try:
    conn.execute("ALTER TABLE incidents ADD COLUMN date TEXT")
    print("Date column added successfully")
except:
    print("Date column already exists")

conn.commit()
conn.close()