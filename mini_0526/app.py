import sqlite3
from flask import Flask, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'secret-key'

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT
    )
    ''')

    # 테스트 계정
    cur.execute('''
    INSERT OR IGNORE INTO users(username, password)
    VALUES ('admin', '1234')
    ''')

    conn.commit()
    conn.close()

    

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    SELECT * FROM users
    WHERE username=? AND password=?
    ''', (username, password))

    user = cur.fetchone()
    conn.close()

    if user:
        session['user'] = username
        return jsonify({'success': True})

    return jsonify({'success': False}), 401


@app.route('/api/contacts', methods=['GET'])
def get_contacts():

    keyword = request.args.get('keyword', '')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    SELECT * FROM contacts
    WHERE name LIKE ?
    ''', (f'%{keyword}%',))

    rows = cur.fetchall()
    conn.close()

    contacts = []

    for row in rows:
        contacts.append({
            'id': row[0],
            'name': row[1],
            'phone': row[2],
            'email': row[3]
        })

    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():

    data = request.get_json()

    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO contacts(name, phone, email)
    VALUES (?, ?, ?)
    ''', (name, phone, email))

    conn.commit()
    conn.close()

    return jsonify({'success': True})



if __name__=="__main__":
    init_db()
    app.run(debug=True)