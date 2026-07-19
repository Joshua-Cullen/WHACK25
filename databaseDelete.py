import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM money")
cursor.execute("DELETE FROM quiz_scores")
conn.commit()
conn.close()
