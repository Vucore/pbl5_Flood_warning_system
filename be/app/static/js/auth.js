// File xử lý đăng nhập và đăng ký
document.addEventListener('DOMContentLoaded', function () {
    // Lấy các phần tử form
    const loginForm = document.getElementById('loginForm');
    const guestAccessBtn = document.getElementById('guestAccessBtn');
    const googleLoginBtn = document.getElementById('googleLoginBtn');
    const adminLoginBtn = document.getElementById('adminLoginBtn');
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
                    const userData = {
                        email: email,
                        isGuest: false,
                        isOnline: true,
                        lastLogin: Date.now()
                    };

                    sessionStorage.setItem('loggedIn', true);
                    sessionStorage.setItem('userEmail', email);
                    try {
                        const response = await fetch(`${API_LOGIN_STATE}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(userData)
                        });

                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.message || 'Cập nhật trạng thái đăng nhập thất bại');
                        }

                        const result = await response.json();
                        if (!result.success) {
                            throw new Error(result.error || 'Cập nhật trạng thái đăng nhập thất bại');
                        }
                    } catch (error) {
                        console.error('Lỗi cập nhật trạng thái đăng nhập:', error);
                        showMessage('error', 'Không thể cập nhật trạng thái đăng nhập. Vui lòng thử lại sau.');
                    }
                    document.getElementById('loginEmail').value = '';
                    loginForm.querySelectorAll('input, button').forEach(el => el.disabled = true);
                    showMessage('success', 'Đăng nhập thành công! Đang chuyển hướng...');

                    setTimeout(() => {
                        window.location.replace('/static/html/index.html');
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

            sessionStorage.setItem('guestIn', true);
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
            showMessage('success', 'Đang truy cập với tư cách khách...');

            setTimeout(() => {
                window.location.replace('/static/html/index.html');
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
                    window.location.replace('/static/html/index.html');
                }, 1000);
            }, 1500);
        });
    }
    // Xử lý đăng nhập bằng Admin
    if (adminLoginBtn) {
        // Khởi tạo Bootstrap modal
        const modal = new bootstrap.Modal(document.getElementById('adminPasswordModal'));
    
        adminLoginBtn.addEventListener('click', function () {
            modal.show();  // Mở modal khi bấm nút "Đăng nhập admin"
        });
    
        document.getElementById('admin-password-submit').addEventListener('click', async function () {
            const password = document.getElementById("admin-password-input").value;
    
            if (!password) {
                alert("Vui lòng nhập mật khẩu.");
                return;
            }
    
            try {
                const response = await fetch(`${API_ADMIN_AUTH}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ password: password })
                });
    
                const data = await response.json();
    
                if (response.ok && data.success) {
                    window.location.replace('/static/html/admin_control.html');
                } else {
                    alert("Mật khẩu không đúng!");
                }
            } catch (error) {
                alert("Lỗi khi xác thực: " + error.message);
            } finally {
                // Reset modal
                document.getElementById("admin-password-input").value = "";
                modal.hide();
            }
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