// Lấy các phần tử DOM cần thiết để cập nhật dữ liệu cảm biến
import { getLatestData } from './socket.js';

const currentTemp = document.getElementById('temperature');
const currentAirPres = document.getElementById('airPressure');
const currentAirHum = document.getElementById('airHumidity');
const currentRainFall = document.getElementById('rainfall');
const currentSoilHum = document.getElementById('soilHumidity');
const currentWaterLevel = document.getElementById('waterLevel');
// let socket = null;
// let isConnected = false;
let previousData = {
    temperature: 0,
    airPressure: 0,
    airHumidity: 0,
    rainfall: 0,
    soilHumidity: 0,
    waterLevel: 0
};

let threSold = {
    tempChange: { value: 38, type: ">"},
    pressureChange: { value: 1000, type: "<"},
    humidityChange: { value: 85, type: ">"},
    rainfallChange: {value: 5, type: ">"},
    soilHumidityChange: {value: 75, type: ">"},
    waterLevelChange: { value: 10, type: ">"},

}


function handleAndShowData(data) {
    try { 
        // Cập nhật dữ liệu cảm biến
        currentTemp.textContent = data.temperature.toFixed(2) + " °C";
        currentAirPres.textContent = data.air_pressure.toFixed(2) + " hPa";
        currentAirHum.textContent = data.air_humidity.toFixed(2) + " %";
        currentRainFall.textContent = data.rainfall.toFixed(2) + " mm/h";
        currentSoilHum.textContent = data.soil_humidity.toFixed(2) + " %";
        currentWaterLevel.textContent = data.water_level.toFixed(2) + " m";
    
        // Cập nhật các thay đổi và cảnh báo
        updateChanges('tempChange', data.temperature, previousData.temperature);
        updateChanges('pressureChange', data.air_pressure, previousData.airPressure);
        updateChanges('humidityChange', data.air_humidity, previousData.airHumidity);
        updateChanges('rainFallChange', data.rainfall, previousData.rainfall);
        updateChanges('soilHumidityChange', data.soil_humidity, previousData.soilHumidity);
        updateChanges('waterLevelChange', data.water_level, previousData.waterLevel);

        checkThresold('tempChange', data.temperature, threSold.tempChange)
        checkThresold('pressureChange', data.air_pressure, threSold.pressureChange)
        checkThresold('humidityChange', data.air_humidity, threSold.humidityChange)
        checkThresold('rainFallChange', data.rainfall, threSold.rainfallChange)
        checkThresold('soilHumidityChange', data.soil_humidity, threSold.soilHumidityChange)
        checkThresold('waterLevelChange', data.water_level, threSold.waterLevelChange)

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
        updateFloodRisk({
            rainfall: data.rainfall,
            water_level: data.water_level,
            soil_humidity: data.soil_humidity,
            air_humidity: data.air_humidity,
            air_pressure: data.air_pressure,
            temperature: data.temperature
        });

    } catch (error) {
        console.error("Lỗi khi xử lý và hiển thị thông số:", error);
    }
}

// Hàm cập nhật sự thay đổi giữa giá trị mới và cũ
function updateChanges(elementId, newValue, oldValue) {
    const change = newValue - oldValue;
    const changeElement = document.getElementById(elementId);
    // console.log("newValue:", newValue, "oldValue:", oldValue);

    if (change > 0) {
        changeElement.style.fontWeight = "normal";
        changeElement.textContent = `⬆ +${change.toFixed(2)} so với lần đo trước`;
        changeElement.style.color = '#28a745'; // Màu xanh cho thay đổi tích cực
    } else if (change < 0) {
        changeElement.style.fontWeight = "normal";
        changeElement.textContent = `⬇ ${change.toFixed(2)} so với lần đo trước`;
        changeElement.style.color = '#dc3545'; // Màu đỏ cho thay đổi tiêu cực
    } else {
        changeElement.style.fontWeight = "normal";
        changeElement.textContent = 'Không có sự thay đổi';
        changeElement.style.color = '#6c757d'; // Màu xám nếu không có thay đổi
    }
}

function checkThresold(elementId, newValue, threSold) {
    const changeElement = document.getElementById(elementId);
    const config = threSold;
    // print(threSold)
    if (!changeElement) {
        console.warn("❌ Không tìm thấy phần tử:", elementId);
        return;
    }

    if (!config) {
        console.warn("❗ Không có ngưỡng cho:", elementId);
        return;
    }

    const { value, type } = config;

    let isWarning = false;
    if (type === ">" && newValue > value) isWarning = true;
    if (type === "<" && newValue < value) isWarning = true;

    if (isWarning) {
        changeElement.style.fontWeight = "bold";
        changeElement.style.color = "red";
        changeElement.textContent = `🚨 Chỉ số ở mức cảnh báo`;
    }
}

setInterval(() => {
    const data = getLatestData();
    if (data) {
        handleAndShowData(data)
    }
}, 5000);


async function updateFloodRisk(sensorData) {
    const response = await fetch(`${API_PREDICT_RISK}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sensorData)
    });
    if (!response.ok) {
        console.error("Lỗi khi gọi API:", response.status, response.statusText);
        return;
    }
    const data = await response.json();
    // data: { risk_score, label, class_idx }

    // Cập nhật nhãn rủi ro
    document.querySelector('.risk-label').textContent = data.label.toUpperCase();

    // Hiển thị phần trăm rủi ro dựa trên risk_score (giá trị 0-1)
    const percent = Math.round(data.risk_score * 100);

    // Cập nhật progress bar
    document.querySelector('.progress-bar').style.width = percent + "%";
    document.querySelector('.progress-bar span').textContent = percent + "%";

    // Đổi màu progress bar theo mức độ
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.background = "#42bc75"; // mặc định an toàn
    if (data.class_idx === 1) progressBar.style.background = "#ffc107"; // chú ý
    if (data.class_idx === 2) progressBar.style.background = "#fd7e14"; // nguy hiểm
    if (data.class_idx === 3) progressBar.style.background = "#dc3545"; // khẩn cấp
}