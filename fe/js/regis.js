document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const username = document.getElementById('username').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const address = document.getElementById('address').value.trim();
            const registerBtn = document.getElementById('register-btn');

            if (!username || !email || !phone || !address) {
                showMessage('error', 'Vui lòng điền đầy đủ thông tin.');
                return;
            }

            const userData = {
                username,
                email,
                phone,
                address
            };

            try {
                // Hiển thị trạng thái loading
                registerBtn.classList.add('btn-loading');
                registerBtn.innerHTML = '<span>' + registerBtn.textContent + '</span>';

                showMessage('info', 'Đang xử lý đăng ký...');
                const result = await sendRegisterRequest(userData);
                if (result['success']) {
                    showMessage('success', 'Đăng ký thành công!');
                    registerForm.querySelectorAll('input, button').forEach(el => el.disabled = true);
                    setTimeout(() => {
                         window.location.replace('login.html');
                    }, 3000); 
                
                } else {
                    registerBtn.classList.remove('btn-loading');
                    registerBtn.textContent = 'Đăng ký';
                    showMessage('error', result['message']);
                }
            } catch (error) {
                registerBtn.classList.remove('btn-loading');
                registerBtn.textContent = 'Đăng ký';
                showMessage('error', error.message || 'Đăng ký thất bại. Vui lòng thử lại sau.');
            }
        });
    }
    
});

// Hàm gửi yêu cầu đăng ký
async function sendRegisterRequest(userData) {
    try {
        const response = await fetch(`${API_REGISTER}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: userData.username,
                email: userData.email,
                phone: userData.phone,
                address: userData.address

            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Đăng ký thất bại.');
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error('Lỗi đăng ký:', error);
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
    if (!message.includes('Đang chuyển hướng')) {
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