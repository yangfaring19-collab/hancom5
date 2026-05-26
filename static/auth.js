// 로그인 폼 제출 이벤트 처리
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // 로그인 성공 - 페이지 새로고침
            messageDiv.innerHTML = `<div class="message success">로그인 성공! 페이지를 이동합니다...</div>`;
            setTimeout(() => {
                window.location.href = '/search';
            }, 1000);
        } else {
            // 로그인 실패
            messageDiv.innerHTML = `<div class="message error">${data.message || '로그인 실패: 아이디 또는 비밀번호를 확인하세요.'}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.innerHTML = `<div class="message error">오류가 발생했습니다: ${error.message}</div>`;
    }
});
