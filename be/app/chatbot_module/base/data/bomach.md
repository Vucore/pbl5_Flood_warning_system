# Thông tin về Bo mạch và Cảm biến cho Hệ thống Cảnh báo Sớm Lũ Lụt

## 0. Các vi mạch, phần cứng, thiết bị, cảm biến được sử dụng trong dự án
- Micro:bit
- ESP8266
- Cảm biến độ ẩm đất
- Cảm biến mưa
- Cảm biến BME280 (đo nhiệt độ không khíkhí, áp suất không khí, độ ẩm không khí)
- Cảm biến siêu âm

## 1. Micro:bit
- **Mô tả**: Micro:bit là bo mạch lập trình nhỏ gọn, được thiết kế cho giáo dục và các dự án IoT. Nó tích hợp CPU ARM Cortex-M4, cảm biến gia tốc, la bàn, và hỗ trợ kết nối Bluetooth.
- **Ứng dụng trong dự án**: 
  - Thu thập dữ liệu từ cảm biến độ ẩm đất hoặc cảm biến mưa thông qua các chân GPIO.
  - Gửi dữ liệu qua Bluetooth hoặc kết nối với mô-đun Wi-Fi (như ESP8266) để truyền dữ liệu đến cơ sở dữ liệu RAG.
  - Phù hợp cho các dự án đơn giản hoặc triển khai tại trường học, khu vực nông thôn.
- **Ưu điểm**: Dễ lập trình (MakeCode, Python), giá rẻ (~15-20 USD), cộng đồng hỗ trợ lớn.
- **Nhược điểm**: Hạn chế về số lượng chân GPIO, không có Wi-Fi tích hợp.

## 2. ESP8266
- **Mô tả**: ESP8266 là mô-đun Wi-Fi giá rẻ, tích hợp vi điều khiển 32-bit, hỗ trợ giao tiếp I2C, SPI, UART. Các phiên bản phổ biến: NodeMCU, ESP-01.
- **Ứng dụng trong dự án**:
  - Kết nối với cảm biến BME280, cảm biến mưa, độ ẩm đất để thu thập dữ liệu thời tiết và thủy văn.
  - Gửi dữ liệu thời gian thực qua Wi-Fi đến cơ sở dữ liệu hoặc API (ví dụ: OpenWeatherMap) để chatbot RAG truy xuất.
  - Xây dựng máy chủ web nhỏ để hiển thị dữ liệu cảm biến.
- **Ưu điểm**: Giá rẻ (~3-7 USD), hỗ trợ Wi-Fi, dễ lập trình qua Arduino IDE.
- **Nhược điểm**: Tiêu thụ điện cao, số lượng chân GPIO hạn chế.

## 3. Cảm biến Độ ẩm Đất
- **Mô tả**: Cảm biến đo độ ẩm đất (soil moisture sensor) sử dụng điện trở hoặc điện dung để xác định độ ẩm trong đất, thường có 2-3 chân (analog hoặc digital).
- **Ứng dụng trong dự án**:
  - Đo độ ẩm đất để đánh giá nguy cơ lũ lụt hoặc khô hạn ở khu vực nông nghiệp.
  - Dữ liệu từ cảm biến được micro:bit hoặc ESP8266 thu thập, cung cấp thông tin cho chatbot RAG về điều kiện đất.
- **Ưu điểm**: Giá rẻ (~1-5 USD), dễ tích hợp, phù hợp cho nông nghiệp thông minh.
- **Nhược điểm**: Cần hiệu chỉnh thường xuyên, dễ bị ăn mòn nếu để ngoài trời lâu.

## 4. Cảm biến Mưa
- **Mô tả**: Cảm biến mưa (rain sensor) phát hiện sự hiện diện của nước mưa thông qua các điện cực nhạy. Thường có đầu ra analog hoặc digital.
- **Ứng dụng trong dự án**:
  - Phát hiện mưa lớn hoặc mưa kéo dài, cung cấp dữ liệu thời gian thực cho hệ thống RAG để cảnh báo ngập lụt.
  - Kết hợp với ESP8266 để gửi cảnh báo qua Wi-Fi.
- **Ưu điểm**: Đơn giản, giá rẻ (~2-5 USD), dễ kết nối với micro:bit hoặc ESP8266.
- **Nhược điểm**: Độ nhạy phụ thuộc vào chất lượng cảm biến, cần bảo vệ khỏi ăn mòn.

## 5. Cảm biến BME280
- **Mô tả**: BME280 là cảm biến môi trường của Bosch, đo nhiệt độ (±1°C), độ ẩm (±3%), áp suất khí quyển (±1 hPa). Hỗ trợ giao tiếp I2C hoặc SPI.
- **Ứng dụng trong dự án**:
  - Thu thập dữ liệu thời tiết (nhiệt độ, độ ẩm, áp suất) để dự báo nguy cơ lũ lụt hoặc bão.
  - Tích hợp với ESP8266 để gửi dữ liệu qua Wi-Fi, cung cấp thông tin cho chatbot RAG.
  - Ước tính độ cao dựa trên áp suất, hỗ trợ xác định khu vực dễ ngập.
- **Ưu điểm**: Độ chính xác cao, kích thước nhỏ, giá hợp lý (~5 USD).
- **Nhược điểm**: Yêu cầu hiệu chỉnh áp suất mực nước biển cho kết quả chính xác.

## 6. Cảm biến Siêu âm
- **Mô tả**: Cảm biến siêu âm (ultrasonic sensor, như HC-SR04) đo khoảng cách bằng sóng siêu âm, thường dùng để đo mực nước hoặc khoảng cách.
- **Ứng dụng trong dự án**:
  - Đo mực nước sông, hồ, hoặc khu vực ngập lụt, cung cấp dữ liệu thời gian thực cho hệ thống RAG.
  - Kết hợp với micro:bit hoặc ESP8266 để gửi cảnh báo khi mực nước vượt ngưỡng.
- **Ưu điểm**: Giá rẻ (~2-5 USD), dễ sử dụng, phù hợp cho đo mực nước.
- **Nhược điểm**: Độ chính xác giảm trong môi trường có nhiều nhiễu hoặc bề mặt không phẳng.

