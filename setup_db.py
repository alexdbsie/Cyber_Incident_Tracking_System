import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,password TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, type TEXT,severity TEXT,description TEXT,status TEXT)""")

conn.commit()
conn.close()

print("Database created successfully")