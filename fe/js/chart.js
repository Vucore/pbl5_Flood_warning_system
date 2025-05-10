let temperatureChart;
let airPressureChart;
let airHumidityChart;
let rainfallChart;
let soilHumidityChart;
let waterLevelChart;

// Khởi tạo các biểu đồ
function initCharts() {
    // Biểu đồ nhiệt độ
    temperatureChart = new Chart(document.getElementById('temperatureChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature (°C)',
                data: [],
                borderColor: '#FF6384',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                }
            }
        }
    });

    // Biểu đồ áp suất không khí
    airPressureChart = new Chart(document.getElementById('airPressureChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Air Pressure (hPa)',
                data: [],
                borderColor: '#36A2EB',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Air Pressure (hPa)'
                    }
                }
            }
        }
    });

    // Biểu đồ độ ẩm không khí
    airHumidityChart = new Chart(document.getElementById('airHumidityChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Air Humidity (%)',
                data: [],
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Air Humidity (%)'
                    }
                }
            }
        }
    });

    // Biểu đồ lượng mưa
    rainfallChart = new Chart(document.getElementById('rainfallChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Rainfall (mm)',
                data: [],
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    }
                }
            }
        }
    });

    // Biểu đồ độ ẩm đất
    soilHumidityChart = new Chart(document.getElementById('soilHumidityChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Soil Humidity (%)',
                data: [],
                borderColor: '#FF9800',
                backgroundColor: 'rgba(255, 152, 0, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Soil Humidity (%)'
                    }
                }
            }
        }
    });

    // Biểu đồ mực nước
    waterLevelChart = new Chart(document.getElementById('waterLevelChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Water Level (cm)',
                data: [],
                borderColor: '#9C27B0',
                backgroundColor: 'rgba(156, 39, 176, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Water Level (cm)'
                    }
                }
            }
        }
    });

    // Hiển thị biểu đồ nhiệt độ mặc định
    document.querySelector('.card-chart[data-chart="temperature"]').classList.add('active');
    document.querySelector('.chart-btn[data-chart="temperature"]').classList.add('active');
}

// Xử lý sự kiện chuyển đổi biểu đồ
document.addEventListener('DOMContentLoaded', function () {
    // Khởi tạo các biểu đồ
    initCharts();

    // Xử lý sự kiện click cho các nút chuyển đổi biểu đồ
    const chartButtons = document.querySelectorAll('.chart-btn');
    chartButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Xóa class active khỏi tất cả các nút
            chartButtons.forEach(btn => btn.classList.remove('active'));
            // Thêm class active cho nút được click
            this.classList.add('active');

            // Ẩn tất cả các biểu đồ
            const charts = document.querySelectorAll('.card-chart');
            charts.forEach(chart => chart.classList.remove('active'));

            // Hiển thị biểu đồ tương ứng
            const chartType = this.getAttribute('data-chart');
            const selectedChart = document.querySelector(`.card-chart[data-chart="${chartType}"]`);
            selectedChart.classList.add('active');
        });
    });
});

// Cập nhật CSS cho card-chart
const style = document.createElement('style');
style.textContent = `
    .card-chart {
        display: none;
        background: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        height: 500px;
        position: relative;
    }
    
    .card-chart.active {
        display: block;
    }
`;
document.head.appendChild(style);

// Cập nhật hàm xử lý dữ liệu WebSocket
function handleWebSocketData(data) {
    try {
        const [temperature, airPressure, airHumidity, rainfall, soilHumidity, waterLevel] = data.split(';').map(Number);

        // Cập nhật biểu đồ nhiệt độ
        updateChart(temperatureChart, temperature);

        // Cập nhật biểu đồ áp suất không khí
        updateChart(airPressureChart, airPressure);

        // Cập nhật biểu đồ độ ẩm không khí
        updateChart(airHumidityChart, airHumidity);

        // Cập nhật biểu đồ lượng mưa
        updateChart(rainfallChart, rainfall);

        // Cập nhật biểu đồ độ ẩm đất
        updateChart(soilHumidityChart, soilHumidity);

        // Cập nhật biểu đồ mực nước
        updateChart(waterLevelChart, waterLevel);
    } catch (error) {
        console.error('Error updating charts:', error);
    }
}

// Hàm cập nhật dữ liệu cho biểu đồ
function updateChart(chart, value) {
    if (!chart) return;

    const time = new Date().toLocaleTimeString();
    chart.data.labels.push(time);
    chart.data.datasets[0].data.push(value);

    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }

    chart.update();
}

// Gọi hàm khởi tạo khi trang web được tải
document.addEventListener('DOMContentLoaded', initCharts); 