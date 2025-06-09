// socket.js
const socket = new WebSocket(`${API_WS}`);
let latestData = null;

let isConnected = false;
let hasData = false;

export function getLatestData() {
    if (hasData && socket && socket.readyState === WebSocket.OPEN)
        return latestData;
    else {
        latestData = null;
        return latestData;
    }
}

socket.addEventListener('open', function(event) {
    console.log("Connected to WebSocket server");
    isConnected = true;
});
socket.addEventListener('message', function(event) {
    if (event.data === "ping") {
        console.log("⚡ Nhận ping từ server, bỏ qua...");
        hasData = false;
        return;
    }
    try {
        hasData = true;
        const parsed = JSON.parse(event.data);
        latestData = parsed; // Cập nhật data mới nhất
        console.log("📦 Dữ liệu mới nhận được:", latestData);
    } catch (e) {
        console.error("❌ Lỗi parse JSON:", e);
    }
});
socket.addEventListener('close', function(event) {
    console.log("Connection closed. Reconnecting...");
    isConnected = false;
    setTimeout(connectWebSocket, 1000); // Tự động kết nối lại sau 1 giây
});

socket.addEventListener('error', function(event) {
    isConnected = false;
    socket.close();
    console.error("WebSocket error:", event);
});
