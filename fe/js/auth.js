// File xử lý đăng nhập và đăng ký
document.addEventListener('DOMContentLoaded', function () {
    // Lấy các phần tử form
    const loginForm = document.getElementById('loginForm');
    const guestAccessBtn = document.getElementById('guestAccessBtn');
    const googleLoginBtn = document.getElementById('googleLoginBtn');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const email = document.getElementById('loginEmail').value.trim();
            const loginBtn = document.getElementById('login-btn');

            if (!email) {
                showMessage('error', 'Vui lòng nhập email.');
                return;
            }

            try {
                // Hiển thị trạng thái loading
                loginBtn.classList.add('btn-loading');
                loginBtn.innerHTML = '<span>' + loginBtn.textContent + '</span>';

                showMessage('info', 'Đang xử lý đăng nhập...');
                const result = await sendLoginRequest(email);

                if (result['success']) {
                    
                    localStorage.setItem('loggedIn', 'true');
                    document.getElementById('loginEmail').value = '';
                    loginForm.querySelectorAll('input, button').forEach(el => el.disabled = true);
                    showMessage('success', 'Đăng nhập thành công! Đang chuyển hướng...');

                    setTimeout(() => {
                        window.location.replace('index.html');
                    }, 1500);
                } else {
                    loginBtn.classList.remove('btn-loading');
                    loginBtn.textContent = 'Đăng nhập';
                    showMessage('error', 'Email không tồn tại trong hệ thống.');
                }
            } catch (error) {
                loginBtn.classList.remove('btn-loading');
                loginBtn.textContent = 'Đăng nhập';
                showMessage('error', error.message || 'Đăng nhập thất bại. Vui lòng thử lại sau.');
            }
        });
    }
   
    // Xử lý truy cập khách
    if (guestAccessBtn) {
        guestAccessBtn.addEventListener('click', function () {
            // Hiển thị trạng thái loading
            guestAccessBtn.classList.add('btn-loading');
            guestAccessBtn.innerHTML = '<span>' + guestAccessBtn.textContent + '</span>';

            localStorage.setItem('guestIn', 'guest');
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
            showMessage('success', 'Đang truy cập với tư cách khách...');

            setTimeout(() => {
                window.location.replace('index.html');
            }, 1000);
        });
    }
    // Xử lý đăng nhập bằng Google
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener('click', function () {
            // Hiển thị trạng thái loading
            googleLoginBtn.classList.add('btn-loading');
            googleLoginBtn.innerHTML = '<span>' + googleLoginBtn.textContent + '</span>';

            showMessage('info', 'Đang chuyển hướng đến trang đăng nhập Google...');

            setTimeout(() => {

                showMessage('success', 'Đăng nhập bằng Google thành công! Đang chuyển hướng...');

                setTimeout(() => {
                    window.location.replace('index.html');
                }, 1000);
            }, 1500);
        });
    }
});


// Hàm gửi yêu cầu đăng nhập
async function sendLoginRequest(email) {
    try {
        const response = await fetch(`${API_LOGIN}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Đăng nhập thất bại.');
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error('Lỗi đăng nhập:', error);
        throw error;
    }
}


// Hàm hiển thị thông báo
function showMessage(type, message) {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;

    // Xóa thông báo cũ
    messageContainer.innerHTML = '';

    // Tạo thông báo mới
    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}-message`;
    messageElement.textContent = message;

    // Thêm vào container
    messageContainer.appendChild(messageElement);

    // Tự động xóa thông báo sau 5 giây (trừ khi là thông báo thành công dẫn đến chuyển trang)
    if (type !== 'success' || !message.includes('chuyển hướng')) {
        setTimeout(() => {
            messageElement.style.opacity = '0';
            setTimeout(() => {
                if (messageContainer.contains(messageElement)) {
                    messageContainer.removeChild(messageElement);
                }
            }, 300);
        }, 5000);
    }
}