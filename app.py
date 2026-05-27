import sqlite3
from flask import Flask, request, session, jsonify, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')
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


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# 페이지 라우트

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('search/index.html')


# 인증 API

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cur.fetchone()
    conn.close()

    if user:
        session['user'] = username
        return jsonify({'success': True, 'message': f'로그인 성공! 환영합니다, {username}님'})

    return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 잘못되었습니다.'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': '로그아웃되었습니다.'})


# 연락처 API

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    keyword = request.args.get('q', request.args.get('keyword', '')).strip()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?',
                (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = cur.fetchall()
    conn.close()

    contacts = [{'id': row[0], 'name': row[1], 'phone': row[2], 'email': row[3]} for row in rows]
    return jsonify({'success': True, 'contacts': contacts, 'count': len(contacts)})


@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()

    if not name or not phone:
        return jsonify({'success': False, 'message': '이름과 전화번호는 필수입니다.'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT id FROM contacts WHERE phone=?', (phone,))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '이미 등록된 전화번호입니다.'}), 400

    cur.execute('INSERT INTO contacts(name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({'success': True, 'message': '연락처가 추가되었습니다.',
                    'contact': {'id': new_id, 'name': name, 'phone': phone, 'email': email}}), 201


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM contacts WHERE id=?', (contact_id,))
    contact = cur.fetchone()

    if not contact:
        conn.close()
        return jsonify({'success': False, 'message': '해당 연락처를 찾을 수 없습니다.'}), 404

    cur.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': '연락처가 삭제되었습니다.'})


# 에러 핸들러

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': '페이지를 찾을 수 없습니다.'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'message': '서버 오류가 발생했습니다.'}), 500


# 실행

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)