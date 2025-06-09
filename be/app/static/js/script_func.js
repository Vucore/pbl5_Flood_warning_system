// Gán sự kiện cho nút dismiss sau khi DOM đã tải xong
document.addEventListener('DOMContentLoaded', function () {
    const dismissButton = document.getElementById('hide-Warning');
    dismissButton.addEventListener('click', function(event) {
        hideWarning(event);
    });
});

// Hàm cập nhật cảnh báo khi nhiệt độ, lượng mưa, mực nước vượt mức nguy hiểm
function updateWarning(temperature, rainfall, waterLevel) {
    let warningMessage = "";
    let warningLevel = "none";

    if (temperature > 30) {
        warningMessage = "⚠️ Cảnh báo: Nhiệt độ cao, vượt quá 30°C!";
        warningLevel = "high";
    } else if (rainfall > 50) {
        warningMessage = "⚠️ Cảnh báo: Lượng mưa cao, nguy cơ lũ lụt!";
        warningLevel = "medium";
    } else if (waterLevel > 100) {
        warningMessage = "⚠️ Cảnh báo: Mực nước rất cao!";
        warningLevel = "high";
    }

    const warningElement = document.getElementById('warning');
    const warningText = warningElement.querySelector('div');

    if (warningMessage) {
        warningElement.style.display = 'flex';
        warningText.textContent = warningMessage;
        warningElement.classList.add(warningLevel); // Thêm lớp cảnh báo tùy theo mức độ
    } else {
        warningElement.style.display = 'none';
    }
}

// Hàm ẩn cảnh báo khi nhấn nút "Dismiss"
function hideWarning(event) {
    // Ngừng hành động mặc định của sự kiện (ngừng việc di chuyển đến liên kết nếu có)
    if (event) {
        event.preventDefault();
    }
    document.getElementById('warning').style.display = 'none';
}



async function logout() {
    const email = sessionStorage.getItem("userEmail");

    if (email) {
        try {
            await fetch(`${API_LOGIN_STATE}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    isGuest: false,
                    isOnline: false,
                    lastLogin: Date.now()
                })
            });
        } catch (err) {
            console.error("Lỗi cập nhật isOnline:", err);
        }
    }
    sessionStorage.removeItem("loggedIn")
    sessionStorage.removeItem("guestIn")
    window.location.replace('login.html');
}