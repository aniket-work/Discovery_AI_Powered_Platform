import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, secret_question TEXT, secret_answer TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, secret_question, secret_answer):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_answer = bcrypt.hashpw(secret_answer.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
              (username, hashed_password, secret_question, hashed_answer))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result[0])
    return False

def get_secret_question(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT secret_question FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def verify_secret_answer(username, answer):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT secret_answer FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(answer.encode('utf-8'), result[0])
    return False

def update_password(username, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    c.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
    conn.commit()
    conn.close()