import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

users = "CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(100) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(100) NOT NULL);"

money = """
CREATE TABLE money (
    money_id INTEGER PRIMARY KEY AUTOINCREMENT,       
    user_id INT NOT NULL,            
    date DATE NOT NULL,    
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    type VARCHAR(50) NOT NULL,
    
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE 
);"""

cursor.execute(users)

cursor.execute(money)

conn.commit()

# Closing the connection
conn.close()

