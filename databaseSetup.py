import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

users = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(100) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(100) NOT NULL);"

money = """
CREATE TABLE IF NOT EXISTS money (
    money_id INTEGER PRIMARY KEY AUTOINCREMENT,       
    user_id INTEGER NOT NULL,            
    date DATE NOT NULL,    
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    type VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE 
);"""

quiz_scores = """
CREATE TABLE IF NOT EXISTS quiz_scores (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);"""

cursor.execute(users)
cursor.execute(money)
cursor.execute(quiz_scores)

conn.commit()
conn.close()
