// Khởi tạo biểu đồ nhiệt độ
import { getLatestData } from './socket.js';

const ctx = document.getElementById('temperatureChart').getContext('2d');
let temperatureChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Mảng thời gian
        datasets: [{
            label: 'Nhiệt độ (°C)',
            data: [], // Mảng giá trị nhiệt độ
            borderColor: '#FF6384',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#FF6384'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 10
            }
        },
        scales: {
            y: {
                min: 15, // Giá trị tối thiểu của trục y
                max: 60, // Giá trị tối đa của trục y
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    stepSize: 5, // Bước nhảy giữa các điểm trên trục y
                    font: {
                        size: 12
                    }
                },
                title: {
                    display: false
                }
            },
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    maxRotation: 45,
                    minRotation: 45,
                    font: {
                        size: 12
                    },
                    maxTicksLimit: 12 // Giới hạn số lượng nhãn trên trục x
                },
                title: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        }
    }
});

// Khởi tạo biểu đồ mực nước
const ctxWater = document.getElementById('waterLevelChart').getContext('2d');
let waterLevelChart = new Chart(ctxWater, {
    type: 'line',
    data: {
        labels: [], // Mảng thời gian
        datasets: [{
            label: 'Mực nước (cm)',
            data: [], // Mảng giá trị mực nước
            borderColor: '#4A90E2', // Màu xanh dương đậm
            backgroundColor: 'rgba(74, 144, 226, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#4A90E2'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 10
            }
        },
        scales: {
            y: {
                min: 0, // Giá trị tối thiểu của trục y
                max: 100, // Giá trị tối đa của trục y
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    stepSize: 10, // Bước nhảy 10cm
                    font: {
                        size: 12
                    }
                },
                title: {
                    display: false
                }
            },
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    maxRotation: 45,
                    minRotation: 45,
                    font: {
                        size: 12
                    },
                    maxTicksLimit: 12
                },
                title: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        }
    }
});

// Khởi tạo biểu đồ áp suất không khí
const ctxAirPressure = document.getElementById('airPressureChart').getContext('2d');
let airPressureChart = new Chart(ctxAirPressure, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Áp suất không khí (hPa)',
            data: [],
            borderColor: '#36A2EB',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#36A2EB'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                min: 950,
                max: 1030,
                ticks: {
                    stepSize: 10
                },
                title: {
                    display: true,
                    text: 'Áp suất không khí (hPa)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Thời gian'
                }
            }
        }
    }
});

// Khởi tạo biểu đồ độ ẩm không khí
const ctxAirHumidity = document.getElementById('airHumidityChart').getContext('2d');
let airHumidityChart = new Chart(ctxAirHumidity, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Độ ẩm không khí (%)',
            data: [],
            borderColor: '#FFCE56',
            backgroundColor: 'rgba(255, 206, 86, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#FFCE56'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                min: 0,
                max: 100,
                ticks: {
                    stepSize: 10
                },
                title: {
                    display: true,
                    text: 'Độ ẩm không khí (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Thời gian'
                }
            }
        }
    }
});

// Khởi tạo biểu đồ lượng mưa
const ctxRainfall = document.getElementById('rainfallChart').getContext('2d');
let rainfallChart = new Chart(ctxRainfall, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Lượng mưa (mm)',
            data: [],
            borderColor: '#4BC0C0',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#4BC0C0'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                min: 0,
                max: 35,
                ticks: {
                    stepSize: 10
                },
                title: {
                    display: true,
                    text: 'Lượng mưa (mm)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Thời gian'
                }
            }
        }
    }
});

// Khởi tạo biểu đồ độ ẩm đất
const ctxSoilHumidity = document.getElementById('soilHumidityChart').getContext('2d');
let soilHumidityChart = new Chart(ctxSoilHumidity, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Độ ẩm đất (%)',
            data: [],
            borderColor: '#9966FF',
            backgroundColor: 'rgba(153, 102, 255, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#9966FF'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                min: 0,
                max: 100,
                ticks: {
                    stepSize: 10
                },
                title: {
                    display: true,
                    text: 'Độ ẩm đất (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Thời gian'
                }
            }
        }
    }
});

// Biến lưu trữ dữ liệu cảm biến
let sensorData = {
    temperature: [],
    airPressure: [],
    airHumidity: [],
    rainfall: [],
    soilHumidity: [],
    waterLevel: []
};

// Hàm cập nhật biểu đồ
function updateTemperatureChart(data) {
    const now = new Date();
    const timeLabel = now.toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    // Thêm dữ liệu mới vào mảng
    sensorData.temperature.push(data.temperature);
    sensorData.airPressure.push(data.air_pressure);
    sensorData.airHumidity.push(data.air_humidity);
    // sensorData.rainfall.push(data.rainfall === "Mưa vừa" ? 50 :
    //     data.rainfall === "Mưa to" ? 80 :
    //         data.rainfall === "Mưa rất to" ? 100 : 30);
    // sensorData.soilHumidity.push(data.soil_humidity === "Ẩm" ? 80 :
    //     data.soil_humidity === "Bình thường" ? 60 :
    //         data.soil_humidity === "Khô" ? 30 : 50);
    sensorData.rainfall.push(data.rainfall);
    sensorData.soilHumidity.push(data.soil_humidity);
    sensorData.waterLevel.push(data.water_level);

    // Thêm nhãn thời gian cho tất cả các biểu đồ
    temperatureChart.data.labels.push(timeLabel);
    waterLevelChart.data.labels.push(timeLabel);
    airPressureChart.data.labels.push(timeLabel);
    airHumidityChart.data.labels.push(timeLabel);
    rainfallChart.data.labels.push(timeLabel);
    soilHumidityChart.data.labels.push(timeLabel);

    // Cập nhật dữ liệu cho tất cả các biểu đồ
    temperatureChart.data.datasets[0].data = sensorData.temperature;
    waterLevelChart.data.datasets[0].data = sensorData.waterLevel;
    airPressureChart.data.datasets[0].data = sensorData.airPressure;
    airHumidityChart.data.datasets[0].data = sensorData.airHumidity;
    rainfallChart.data.datasets[0].data = sensorData.rainfall;
    soilHumidityChart.data.datasets[0].data = sensorData.soilHumidity;

    // Giới hạn số điểm dữ liệu (hiển thị 12 điểm - tương đương 1 phút dữ liệu)
    const maxDataPoints = 12;
    if (temperatureChart.data.labels.length > maxDataPoints) {
        temperatureChart.data.labels.shift();
        waterLevelChart.data.labels.shift();
        airPressureChart.data.labels.shift();
        airHumidityChart.data.labels.shift();
        rainfallChart.data.labels.shift();
        soilHumidityChart.data.labels.shift();
        sensorData.temperature.shift();
        sensorData.airPressure.shift();
        sensorData.airHumidity.shift();
        sensorData.rainfall.shift();
        sensorData.soilHumidity.shift();
        sensorData.waterLevel.shift();
    }

    // Cập nhật tất cả các biểu đồ
    temperatureChart.update('none');
    waterLevelChart.update('none');
    airPressureChart.update('none');
    airHumidityChart.update('none');
    rainfallChart.update('none');
    soilHumidityChart.update('none');
}

// Kết nối với WebSocket để nhận dữ liệu thời gian thực
// let chartSocket = new WebSocket(`${API_CHART}`);

// chartSocket.onmessage = function (event) {
//     if (event.data === "ping") {
//         return;
//     }
//     try {
//         // Parse dữ liệu JSON
//         const data = JSON.parse(event.data);

//         // Kiểm tra dữ liệu hợp lệ
//         if (data && data.temperature !== undefined) {
//             updateTemperatureChart(data);
//             console.log("Dữ liệu biểu đồ:", data);
//         }
//     } catch (error) {
//         console.error("Lỗi khi xử lý dữ liệu biểu đồ:", error);
//     }
// };

// chartSocket.onclose = function () {
//     console.log("Mất kết nối WebSocket cho biểu đồ. Đang kết nối lại...");
//     setTimeout(() => {
//         chartSocket = new WebSocket(`${API_CHART}`);
//     }, 1000);
// };

setInterval(() => {
    const data = getLatestData();
    if (data) {
        updateTemperatureChart(data)
    }
}, 5000);


document.addEventListener('DOMContentLoaded', function () {
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