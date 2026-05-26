# 📋 연락처 관리 시스템

## 한컴AI아카데미 5기 - Git 실습 & 팀 협업 프로젝트

---

## 🎯 프로젝트 개요

Flask 기반의 **연락처 관리 시스템**으로, 로그인 인증과 주소록 CRUD 기능을 제공합니다.  
팀 협업 프로세스와 Git 브랜치 전략을 학습하기 위한 프로젝트입니다.

### 핵심 기능
- ✅ 사용자 로그인/로그아웃 (세션 기반)
- ✅ 연락처 목록 조회
- ✅ 연락처 검색 (이름, 전화번호, 이메일)
- ✅ 새 연락처 추가
- ✅ 연락처 삭제
- ✅ 전화번호 자동 포매팅 (010-1234-5678 형식)

---

## 👥 팀 구성

| 역할 | 담당자 | 브랜치 | 담당 파일 |
|------|--------|--------|----------|
| **백엔드 & DB** | 김호림 | `feature/auth` | `app.py` |
| **프론트엔드 & UI** | 김유성 | `feature/search` | `templates/`, `static/` |

---

## 📁 프로젝트 구조

```
hancom5/
├── app.py                      # Flask 애플리케이션 (팀원 A)
├── database.db                 # SQLite 데이터베이스
├── README.md                   # 프로젝트 문서
├── login.txt                   # 테스트 계정 정보
│
├── templates/                  # HTML 템플릿 (Jinja2)
│   ├── base.html              # 공통 레이아웃
│   ├── index.html             # 로그인 페이지
│   ├── auth/
│   │   └── login.html         # 대체 로그인 페이지
│   └── search/
│       └── index.html         # 연락처 관리 페이지
│
├── static/                     # 정적 파일
│   ├── app.js                 # (기존)
│   ├── auth.js                # 로그인 JavaScript
│   └── search.js              # 연락처 관리 JavaScript
│
└── .git/                       # Git 저장소
```

---

## 🛠 기술 스택

### 백엔드
- **Framework**: Flask (Python)
- **Database**: SQLite3
- **Authentication**: Session-based

### 프론트엔드
- **Markup**: HTML5 + Jinja2 템플릿
- **Styling**: CSS3 (그래디언트, 반응형)
- **Interaction**: Vanilla JavaScript (Fetch API)
- **Security**: XSS 방지 처리

---

## 🔄 Git 브랜치 전략

```
main (최종 완성본 - 직접 커밋 금지)
  ↓
develop (기준 브랜치 - 직접 커밋 금지)
  ├─ feature/auth (백엔드 작업)
  └─ feature/search (프론트엔드 작업)
```

### 작업 프로세스

**1단계: 작업 시작**
```bash
git checkout develop
git pull origin develop      # 최신 상태 유지
git checkout -b feature/xxx  # 기능 브랜치 생성
```

**2단계: 기능 개발 및 커밋**
```bash
# 코드 작성 및 테스트
git add .
git commit -m "feat: 기능 설명"
git push -u origin feature/xxx
```

**3단계: 병합 (Merge)**
- 첫 번째 병합: PR 생성 및 리뷰
- 두 번째 병합: **로컬에서 충돌 해결** 후 진행
```bash
git checkout develop
git pull origin develop
git merge feature/xxx       # 충돌 발생 가능
# 충돌 해결 후
git add .
git commit -m "merge: feature/xxx → develop"
git push origin develop
```

---

## 🚀 설치 및 실행 방법

### 1단계: 환경 준비
```bash
# 리포지토리 클론
git clone https://github.com/yangfaring19-collab/hancom5.git
cd hancom5

# Python 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate

# 필요한 패키지 설치
pip install flask
```

### 2단계: 데이터베이스 초기화
```bash
# (팀원 A가 구현할 부분)
python app.py  # 첫 실행 시 database.db와 테이블 생성
```

### 3단계: 서버 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

---

## 🔐 테스트 계정

| 아이디 | 비밀번호 |
|--------|----------|
| admin  | 1234     |

---

## 📡 API 문서

### 인증 API

#### POST /api/login
로그인 요청 (세션 생성)

**Request**
```json
{
  "username": "admin",
  "password": "1234"
}
```

**Response (성공)**
```json
{
  "success": true,
  "message": "로그인 성공"
}
```

#### POST /api/logout
로그아웃 요청 (세션 제거)

**Response (성공)**
```json
{
  "success": true,
  "message": "로그아웃 성공"
}
```

---

### 연락처 API

#### GET /api/contacts
연락처 전체 조회 또는 검색

**Query Parameters**
- `q` (선택): 검색어 (LIKE 쿼리 사용)

**Request 예시**
```
GET /api/contacts
GET /api/contacts?q=김철수
GET /api/contacts?q=010-1234
```

**Response (성공)**
```json
{
  "success": true,
  "contacts": [
    {
      "id": 1,
      "name": "김철수",
      "phone": "010-1234-5678",
      "email": "kim@example.com"
    },
    {
      "id": 2,
      "name": "이영희",
      "phone": "010-9876-5432",
      "email": "lee@example.com"
    }
  ]
}
```

#### POST /api/contacts
새 연락처 추가

**Request**
```json
{
  "name": "박민준",
  "phone": "010-5555-5555",
  "email": "park@example.com"
}
```

**Response (성공)**
```json
{
  "success": true,
  "message": "연락처가 추가되었습니다",
  "contact": {
    "id": 3,
    "name": "박민준",
    "phone": "010-5555-5555",
    "email": "park@example.com"
  }
}
```

#### DELETE /api/contacts/<id>
연락처 삭제

**Request 예시**
```
DELETE /api/contacts/3
```

**Response (성공)**
```json
{
  "success": true,
  "message": "연락처가 삭제되었습니다."
}
```

**Response (실패 - 없는 ID)**
```json
{
  "success": false,
  "message": "해당 연락처를 찾을 수 없습니다."
}
```

---

## 📱 사용 방법

### 1. 로그인
- 메인 페이지(`/`)에서 아이디/비밀번호 입력
- "로그인" 버튼 클릭
- 성공 시 자동으로 `/search` 페이지로 이동

### 2. 연락처 검색
- 검색창에 **이름, 전화번호, 이메일** 입력
- "검색" 버튼 클릭 또는 엔터 키
- "전체보기" 버튼으로 필터 초기화

### 3. 연락처 추가
- "새 연락처 추가" 폼에 정보 입력
- **전화번호는 입력 중 자동으로 포매팅됨** (예: 01012345678 → 010-1234-5678)
- "추가" 버튼 클릭
- 목록이 자동으로 새로고침됨

### 4. 연락처 삭제
- 연락처 목록의 "관리" 컬럼에서 "삭제" 버튼 클릭
- 확인 대화상자에서 "확인" 선택
- 목록이 자동으로 새로고침되고 연락처 삭제됨

### 5. 로그아웃
- 우측 상단 "로그아웃" 버튼 클릭
- 로그인 페이지로 이동

---

## ✅ 완성 체크리스트

### 팀원 A (백엔드)
- [ ] SQLite 데이터베이스 설계
- [ ] users, contacts 테이블 생성
- [ ] 테스트 계정(admin/1234) 삽입
- [ ] POST /api/login 구현
- [ ] POST /api/logout 구현
- [ ] GET /api/contacts 구현 (LIKE 검색 포함)
- [ ] POST /api/contacts 구현
- [ ] 라우트 설정 (/, /search, /auth/login)
- [ ] 정적 파일 라우팅 확인

### 팀원 B (프론트엔드) ✅
- [x] base.html 공통 레이아웃
- [x] templates/auth/login.html
- [x] static/auth.js (로그인 API 호출)
- [x] templates/search/index.html
- [x] static/search.js (검색, 추가, 로그아웃)
- [x] CSS 스타일링 (반응형)
- [x] XSS 방지 처리
- [x] **연락처 삭제 기능** (DELETE API)
- [x] **전화번호 자동 포매팅** (010-1234-5678 형식)

---

## 🐛 트러블슈팅

### 404 에러: `/api/contacts not found`
→ 팀원 A가 Flask 라우트를 아직 구현하지 않음

### "템플릿을 찾을 수 없음" 에러
→ Flask의 templates 폴더 경로 확인
```python
app = Flask(__name__, template_folder='templates')
```

### 정적 파일(JS, CSS) 로드 실패
→ Flask의 static 폴더 경로 확인
```python
app = Flask(__name__, static_folder='static')
```

### CORS 에러
→ 프론트엔드와 백엔드가 같은 포트에서 실행되므로 일반적으로 발생하지 않음

---

## 📚 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [SQLite3 Python 문서](https://docs.python.org/ko/3/library/sqlite3.html)
- [Jinja2 템플릿 문서](https://jinja.palletsprojects.com/)
- [Fetch API MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API)

---

## 📝 License

한컴AI아카데미 5기 교육용

---

## 👤 팀 정보

**프로젝트명**: 연락처 관리 시스템  
**기간**: 2026년 5월  
**목표**: Git 협업 프로세스 및 팀 개발 경험 습득


