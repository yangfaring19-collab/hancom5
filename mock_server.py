"""
Mock Flask 서버
프론트엔드 테스트용으로 API 응답을 시뮬레이션합니다.
팀원 A의 app.py가 완성되면 이 파일은 제거됩니다.
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'test-secret-key-for-frontend-testing'

# 테스트용 데이터
test_user = {'username': 'admin', 'password': '1234'}
contacts_db = [
    {'id': 1, 'name': '김철수', 'phone': '010-1234-5678', 'email': 'kim@example.com'},
    {'id': 2, 'name': '이영희', 'phone': '010-9876-5432', 'email': 'lee@example.com'},
    {'id': 3, 'name': '박민준', 'phone': '010-5555-5555', 'email': 'park@example.com'},
]
contact_id_counter = 4

print("=" * 60)
print("🚀 Mock Flask 서버 시작 (프론트엔드 테스트용)")
print("=" * 60)
print(f"⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📝 테스트 계정: admin / 1234")
print(f"📱 샘플 연락처: {len(contacts_db)}개")
print(f"🌐 URL: http://localhost:5000")
print("=" * 60)


# ===================== 페이지 라우트 =====================

@app.route('/')
def index():
    """로그인 페이지"""
    return render_template('index.html')


@app.route('/search')
def search():
    """연락처 관리 페이지"""
    if 'user' not in session:
        return redirect('/')
    return render_template('search/index.html')


# ===================== 인증 API =====================

@app.route('/api/login', methods=['POST'])
def api_login():
    """로그인 API"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    print(f"\n🔐 로그인 시도: {username}")
    
    if username == test_user['username'] and password == test_user['password']:
        session['user'] = username
        print(f"✅ 로그인 성공: {username}")
        return jsonify({
            'success': True,
            'message': f'로그인 성공! 환영합니다, {username}님'
        }), 200
    else:
        print(f"❌ 로그인 실패: 잘못된 자격증명")
        return jsonify({
            'success': False,
            'message': '아이디 또는 비밀번호가 잘못되었습니다.'
        }), 401


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """로그아웃 API"""
    user = session.get('user', 'Unknown')
    print(f"\n🚪 로그아웃: {user}")
    
    session.pop('user', None)
    return jsonify({
        'success': True,
        'message': '로그아웃되었습니다.'
    }), 200


# ===================== 연락처 API =====================

@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    """연락처 조회 또는 검색"""
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        print(f"\n🔍 연락처 검색: '{search_query}'")
        # LIKE 검색 시뮬레이션
        filtered = [
            c for c in contacts_db
            if search_query.lower() in c['name'].lower()
            or search_query in c['phone']
            or search_query.lower() in c['email'].lower()
        ]
        print(f"   결과: {len(filtered)}개 발견")
        return jsonify({
            'success': True,
            'contacts': filtered,
            'count': len(filtered)
        }), 200
    else:
        print(f"\n📇 전체 연락처 조회: {len(contacts_db)}개")
        return jsonify({
            'success': True,
            'contacts': contacts_db,
            'count': len(contacts_db)
        }), 200


@app.route('/api/contacts', methods=['POST'])
def api_add_contact():
    """새 연락처 추가"""
    global contact_id_counter
    
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    
    print(f"\n➕ 새 연락처 추가: {name}")
    
    # 유효성 검사
    if not name or not phone or not email:
        print(f"   ❌ 입력 오류: 필수 항목 누락")
        return jsonify({
            'success': False,
            'message': '모든 필드를 입력하세요.'
        }), 400
    
    # 중복 검사
    if any(c['phone'] == phone for c in contacts_db):
        print(f"   ❌ 중복 오류: 이미 존재하는 전화번호")
        return jsonify({
            'success': False,
            'message': '이미 등록된 전화번호입니다.'
        }), 400
    
    # 새 연락처 추가
    new_contact = {
        'id': contact_id_counter,
        'name': name,
        'phone': phone,
        'email': email
    }
    contacts_db.append(new_contact)
    contact_id_counter += 1
    
    print(f"   ✅ 추가 성공 (ID: {new_contact['id']})")
    
    return jsonify({
        'success': True,
        'message': '연락처가 추가되었습니다.',
        'contact': new_contact
    }), 201


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    """연락처 삭제"""
    global contacts_db
    
    print(f"\n🗑️ 연락처 삭제: ID {contact_id}")
    
    # 연락처 찾기
    contact = next((c for c in contacts_db if c['id'] == contact_id), None)
    
    if not contact:
        print(f"   ❌ 찾을 수 없음: ID {contact_id}")
        return jsonify({
            'success': False,
            'message': '해당 연락처를 찾을 수 없습니다.'
        }), 404
    
    # 삭제
    contacts_db = [c for c in contacts_db if c['id'] != contact_id]
    print(f"   ✅ 삭제 성공: {contact['name']} (ID: {contact_id})")
    
    return jsonify({
        'success': True,
        'message': '연락처가 삭제되었습니다.'
    }), 200


# ===================== 정적 파일 =====================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """정적 파일 제공"""
    return send_from_directory('static', filename)


# ===================== 에러 핸들러 =====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': '페이지를 찾을 수 없습니다.'
    }), 404


@app.errorhandler(500)
def server_error(error):
    print(f"\n🔴 서버 오류: {str(error)}")
    return jsonify({
        'success': False,
        'message': '서버 오류가 발생했습니다.'
    }), 500


# ===================== 실행 =====================

if __name__ == '__main__':
    print("\n💡 팁:")
    print("   - 테스트 계정: admin / 1234")
    print("   - 샘플 연락처를 미리 준비했습니다")
    print("   - 추가, 검색 기능을 테스트할 수 있습니다")
    print("   - app.py가 완성되면 이 파일을 삭제하세요\n")
    
    app.run(
        debug=True,
        host='localhost',
        port=5000,
        use_reloader=False  # 자동 재시작 비활성화
    )
