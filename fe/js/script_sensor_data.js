const currentTemp = document.getElementById('temperature');
const currentAirPres = document.getElementById('airPressure');
const currentAirHum = document.getElementById('airHumidity');
const currentRainFall = document.getElementById('rainfall');
const currentSoilHum = document.getElementById('soilHumidity');
const currentWaterLevel = document.getElementById('waterLevel');

let socket = null;
let isConnected = false;

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
        console.log("Received data:", event.data);
        if (event.data === "ping") {
            console.log("⚡ Nhận ping từ server, bỏ qua...");
            return;
        }
        try {
            const data = JSON.parse(event.data); // Chuyển đổi JSON thành object
    
            currentTemp.textContent = data.temperature.toFixed(2);
            currentAirPres.textContent = data.air_pressure.toFixed(2);
            currentAirHum.textContent = data.air_humidity.toFixed(2);
            currentRainFall.textContent = data.rainfall;
            currentSoilHum.textContent = data.soil_humidity;
            currentWaterLevel.textContent = data.water_level.toFixed(2);

        } catch (error) {
            console.error("Error parsing JSON or updating values:", error);
        }
    });

    socket.addEventListener('close', function(event) {
        console.log("Connection closed. Reconnecting...");
        isConnected = false;
        setTimeout(connectWebSocket, 1000);
    });

    socket.addEventListener('error', function(event) {
        console.error("WebSocket error:", event);
    });
}

// Khởi tạo kết nối
connectWebSocket();
setInterval(function() {
    if (!isConnected) {
        console.log("Checking connection...");
        connectWebSocket();
    }
}, 5000);