// Lấy các phần tử DOM cần thiết để cập nhật dữ liệu cảm biến
const currentTemp = document.getElementById('temperature');
const currentAirPres = document.getElementById('airPressure');
const currentAirHum = document.getElementById('airHumidity');
const currentRainFall = document.getElementById('rainfall');
const currentSoilHum = document.getElementById('soilHumidity');
const currentWaterLevel = document.getElementById('waterLevel');

let socket = null;
let isConnected = false;
let previousData = {
    temperature: 0,
    airPressure: 0,
    airHumidity: 0,
    rainfall: 0,
    soilHumidity: 0,
    waterLevel: 0
};

// Hàm kết nối WebSocket
function connectWebSocket() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        return;
    }

    socket = new WebSocket('ws://localhost:8000/ws');

    socket.addEventListener('open', function(event) {
        console.log("Connected to WebSocket server");
        isConnected = true;
    });

    socket.addEventListener('message', function(event) {
        if (event.data === "ping") {
            console.log("⚡ Nhận ping từ server, bỏ qua...");
            return;
        }
        try {
            const data = JSON.parse(event.data); // Chuyển đổi JSON thành object
            
            
            // Cập nhật dữ liệu cảm biến
            currentTemp.textContent = data.temperature.toFixed(2) + " °C";
            currentAirPres.textContent = data.air_pressure.toFixed(2) + " hPa";
            currentAirHum.textContent = data.air_humidity.toFixed(2) + " %";
            currentRainFall.textContent = data.rainfall;
            currentSoilHum.textContent = data.soil_humidity;
            currentWaterLevel.textContent = data.water_level.toFixed(2) + " m";

            // Cập nhật các thay đổi và cảnh báo
            updateChanges('tempChange', data.temperature, previousData.temperature);
            updateChanges('pressureChange', data.air_pressure, previousData.airPressure);
            updateChanges('humidityChange', data.air_humidity, previousData.airHumidity);
            // updateChanges('rainfallChange', data.rainfall, previousData.rainfall);
            // updateChanges('soilHumidityChange', data.soil_humidity, previousData.soilHumidity);
            updateChanges('waterLevelChange', data.water_level, previousData.waterLevel);

            // updateWarning(data.temperature, data.rainfall, data.water_level);
            // updateCharts(data.temperature, data.rainfall, data.water_level, data.air_humidity, data.soil_humidity);

            // Cập nhật giá trị trước đó
            previousData = {
                temperature: data.temperature,
                airPressure: data.air_pressure,
                airHumidity: data.air_humidity,
                rainfall: data.rainfall,
                soilHumidity: data.soil_humidity,
                waterLevel: data.water_level
            };
            
            // console.log(previousData);

        } catch (error) {
            console.error("Error parsing JSON or updating values:", error);
        }
    });

    socket.addEventListener('close', function(event) {
        console.log("Connection closed. Reconnecting...");
        isConnected = false;
        setTimeout(connectWebSocket, 1000); // Tự động kết nối lại sau 1 giây
    });

    socket.addEventListener('error', function(event) {
        console.error("WebSocket error:", event);
    });
}

// Hàm cập nhật sự thay đổi giữa giá trị mới và cũ
function updateChanges(elementId, newValue, oldValue) {
    const change = newValue - oldValue;
    const changeElement = document.getElementById(elementId);
    // console.log("newValue:", newValue, "oldValue:", oldValue);
    if (change > 0) {
        changeElement.textContent = `⬆ +${change.toFixed(2)} so với ngày hôm qua`;
        changeElement.style.color = '#28a745'; // Màu xanh cho thay đổi tích cực
    } else if (change < 0) {
        changeElement.textContent = `⬇ ${change.toFixed(2)} so với ngày hôm qua`;
        changeElement.style.color = '#dc3545'; // Màu đỏ cho thay đổi tiêu cực
    } else {
        changeElement.textContent = 'Không có sự thay đổi';
        changeElement.style.color = '#6c757d'; // Màu xám nếu không có thay đổi
    }
}

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
// Hàm ẩn cảnh báo khi nhấn nút "Dismiss"
function hideWarning(event) {
    // Ngừng hành động mặc định của sự kiện (ngừng việc di chuyển đến liên kết nếu có)
    if (event) {
        event.preventDefault();
    }
    
    document.getElementById('warning').style.display = 'none';
}

// Gán sự kiện cho nút dismiss sau khi DOM đã tải xong
document.addEventListener('DOMContentLoaded', function () {
    const dismissButton = document.getElementById('hide-Warning');
    dismissButton.addEventListener('click', function(event) {
        hideWarning(event);
    });
});


// Khởi tạo kết nối WebSocket
connectWebSocket();

// Kiểm tra kết nối định kỳ nếu chưa kết nối
setInterval(function() {
    if (!isConnected) {
        console.log("Checking connection...");
        connectWebSocket();
    }
}, 5000);
