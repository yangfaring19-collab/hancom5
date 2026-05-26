// 페이지 로드 시 전체 연락처 목록 조회
document.addEventListener('DOMContentLoaded', () => {
    loadContacts();
    
    // 전화번호 입력 필드에 자동 포매팅 추가
    const phoneInput = document.getElementById('contactPhone');
    phoneInput.addEventListener('input', (e) => {
        e.target.value = formatPhoneNumber(e.target.value);
    });
});

// 전체 연락처 조회 함수
async function loadContacts(query = '') {
    const contactsBody = document.getElementById('contactsBody');
    
    try {
        let url = '/api/contacts';
        if (query) {
            url += `?q=${encodeURIComponent(query)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {
            const contacts = data.contacts || [];
            
            if (contacts.length === 0) {
                contactsBody.innerHTML = '<tr class="no-data"><td colspan="4">연락처가 없습니다.</td></tr>';
            } else {
                // 테이블 동적 생성
                contactsBody.innerHTML = contacts.map(contact => `
                    <tr>
                        <td>${escapeHtml(contact.name)}</td>
                        <td>${escapeHtml(contact.phone)}</td>
                        <td>${escapeHtml(contact.email)}</td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-delete" onclick="deleteContact(${contact.id})">삭제</button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }
        } else {
            contactsBody.innerHTML = '<tr class="no-data"><td colspan="4">연락처를 불러올 수 없습니다.</td></tr>';
            showMessage('error', '연락처 조회에 실패했습니다.');
        }
    } catch (error) {
        console.error('Error:', error);
        contactsBody.innerHTML = '<tr class="no-data"><td colspan="4">오류가 발생했습니다.</td></tr>';
        showMessage('error', `오류: ${error.message}`);
    }
}

// 검색 버튼 이벤트
document.getElementById('searchBtn').addEventListener('click', () => {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    if (query) {
        loadContacts(query);
    } else {
        showMessage('error', '검색어를 입력하세요.');
    }
});

// 검색 입력창에서 엔터 키 처리
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('searchBtn').click();
    }
});

// 전체보기 버튼 이벤트
document.getElementById('resetBtn').addEventListener('click', () => {
    document.getElementById('searchInput').value = '';
    loadContacts();
    showMessage('info', '전체 연락처를 표시합니다.');
});

// 새 연락처 추가 폼 제출
document.getElementById('addContactForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('contactName').value;
    const phone = document.getElementById('contactPhone').value;
    const email = document.getElementById('contactEmail').value;

    try {
        const response = await fetch('/api/contacts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                phone: phone,
                email: email
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('success', '연락처가 추가되었습니다!');
            document.getElementById('addContactForm').reset();
            loadContacts(); // 목록 새로고침
        } else {
            showMessage('error', data.message || '연락처 추가에 실패했습니다.');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('error', `오류: ${error.message}`);
    }
});

// 로그아웃 버튼 이벤트
document.getElementById('logoutBtn').addEventListener('click', async () => {
    if (confirm('정말 로그아웃하시겠습니까?')) {
        try {
            const response = await fetch('/api/logout', {
                method: 'POST'
            });

            if (response.ok) {
                showMessage('success', '로그아웃되었습니다. 페이지를 이동합니다...');
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showMessage('error', '로그아웃에 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('error', `오류: ${error.message}`);
        }
    }
});

// 메시지 표시 함수
function showMessage(type, message) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="message ${type}">${message}</div>`;
    
    // 3초 후 자동으로 메시지 제거
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 3000);
}

// HTML 특수문자 이스케이프 (XSS 방지)
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// 전화번호 포매팅 함수 (예: 01012345678 → 010-1234-5678)
function formatPhoneNumber(value) {
    // 숫자만 추출
    const numbers = value.replace(/\D/g, '');
    
    // 10자 또는 11자일 때만 포매팅
    if (numbers.length === 10) {
        return numbers.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
    } else if (numbers.length === 11) {
        return numbers.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
    }
    
    // 포매팅할 수 없으면 그대로 반환
    return value.substring(0, 13); // 최대 길이 제한
}

// 연락처 삭제 함수
async function deleteContact(contactId) {
    if (!confirm('정말 이 연락처를 삭제하시겠습니까?')) {
        return;
    }

    try {
        const response = await fetch(`/api/contacts/${contactId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('success', '연락처가 삭제되었습니다!');
            loadContacts(); // 목록 새로고침
        } else {
            showMessage('error', data.message || '연락처 삭제에 실패했습니다.');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('error', `오류: ${error.message}`);
    }
}
