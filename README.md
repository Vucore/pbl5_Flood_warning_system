# 🌊 PBL5 - Flood Warning System

Đồ án Kỹ thuật máy tính - Cảnh báo lũ lụt sử dụng dữ liệu cảm biến thời gian thực và Chatbot AI.

---

## 📦 Thiết lập môi trường

### ⚙️ 1. Tạo môi trường ảo
```bash
# Mở terminal tại thư mục gốc dự án
cd PBL5_Flood_warning_system

# Tạo và kích hoạt môi trường ảo
python -m venv venv
venv\Scripts\activate  # Dành cho Windows
# source venv/bin/activate  # Dành cho MacOS/Linux

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Truy cập thư mục backend
cd be
```

---

## 🚀 Cách chạy server

### ✅ Cách 1: Chạy **2 module riêng biệt**

#### 🌐 Module chính (WebSocket, data, function)
```bash
uvicorn app.data_module.start_websocket:api --reload --port 8000
```

#### 🤖 Module Chatbot
```bash
uvicorn app.chatbot_module.start_chatbot:chatbot --reload --port 8001
```

---

### ✅ Cách 2: Chạy đồng thời cả 2 module qua `main`
```bash
uvicorn app.main:app --reload --port 8000
uvicorn app.main:app --host 0.0.0.0 --port 8000

```

---

## 🧪 Fake dữ liệu cảm biến (phục vụ test)

```bash
# Từ thư mục gốc dự án
python fake_data.py
```

---

## 🤖 Cài đặt và chạy mô hình Ollama với LLaMA3

### 1. Cài đặt Ollama:
```bash
# Tải và cài đặt Ollama (tùy hệ điều hành)
https://ollama.com/download
```

### 2. Tải model llama3:
```bash
ollama pull llama3
```

### 3. Chạy server Ollama:
```bash
ollama run llama3
```

> ✅ Ollama sẽ khởi chạy một local LLM server mặc định tại `http://localhost:11434`.

---

## 🔥 Thiết lập Firebase Realtime Database

### 1. Tạo dự án Firebase:
1. Truy cập [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" (hoặc "Add project")
3. Đặt tên dự án (ví dụ: "flood-warning-system")
4. Làm theo các bước còn lại để tạo dự án

### 2. Thiết lập Realtime Database:
1. Trong Firebase Console, chọn dự án vừa tạo
2. Vào Realtime Database trong menu bên trái
3. Click "Create Database"
4. Chọn vị trí server gần nhất
5. Bắt đầu ở Test mode để phát triển

### 3. Lấy credentials:
1. Vào Project Settings (bánh răng cạnh Project Overview)
2. Tab Service accounts
3. Click "Generate New Private Key"
4. Lưu file JSON được tải về vào thư mục `/be`
5. Đổi tên file trong .env

### 4. Cấu trúc dữ liệu Firebase:
```json
{
  "sensor_data": {
    "timestamp_key": {
      "temperature": number,
      "air_pressure": number,
      "air_humidity": number,
      "rainfall": number,
      "soil_humidity": number,
      "water_level": number,
    }
  }
}
```

---

## 🤖 Cấu trúc dữ liệu Chatbot

### 1. File `context.json`:
Chứa các mẫu câu và chủ đề để phân loại tin nhắn với RAG:
```json
[
  {
    "tag": "chat",
    "patterns": [
      "Chào bạn",
      "Bạn khỏe không?",
      "Bạn tên là gì?"
      // Thêm các mẫu câu chat thông thường
    ]
  },
  {
    "tag": "simple",
    "patterns": [
      "Nguyên nhân chính gây ra lũ lụt là gì?",
      "Lũ lụt ảnh hưởng thế nào đến nông nghiệp?"
      // Thêm các câu hỏi về lũ lụt
    ]
  },
  {
    "tag": "call",
    "patterns": [
      "Gửi cảnh báo tới người dân",
      "Gửi email thông báo ngập lụt"
      // Thêm các yêu cầu gửi cảnh báo
    ]
  }
]
```

### 2. File `responses.json`:
Chứa các câu trả lời tương ứng với các tag:
```json
[
  {
    "tag": "greeting",
    "patterns": [
      "Chào bạn",
      "Xin chào"
    ],
    "responses": [
      "Xin chào! Tôi là trợ lý cảnh báo lũ lụt. Bạn cần giúp đỡ gì?",
      "Chào bạn! Tôi có thể giúp gì về nguy cơ lũ lụt?"
    ]
  },
  {
    "tag": "flood_info",
    "patterns": [
      "Lũ lụt là gì?",
      "Nguyên nhân của lũ lụt là gì?"
    ],
    "responses": [
      "Lũ lụt xảy ra khi nước dâng cao và tràn vào đất liền...",
      "Lũ lụt có thể xảy ra do mưa lớn, tan băng..."
    ]
  }
]
```

---

## 🛠️ Công nghệ sử dụng

- **FastAPI**: Framework backend chính.
- **WebSocket**: Giao tiếp thời gian thực.
- **Ollama**: Chạy mô hình LLaMA3 cục bộ.
- **Chroma**: Vector database để lưu trữ và truy vấn embedding.
- **LangChain**: Xây dựng pipeline cho chatbot AI.
- **Huggingface Transformers**: Sử dụng embedding Vietnamese custom từ Huggingface.

---

## 📁 Cấu trúc thư mục

```
PBL5_Flood_warning_system/
│
├── be/                         # Backend FastAPI
│   ├── app/
│   │   ├── chatbot_module/
│   │   ├── data_module/
│   │   └── main.py             # Tích hợp cả websocket và chatbot
│   └── ...
│
├── fe/                        
│   ├── css/
│   ├── html/
│   ├── js/
│   └── ...
│   
│ 
├── Iot
├── venv/
├── .gitignore
├── fake_data.py               # Script tạo dữ liệu cảm biến giả
├── README.md
└── requirements.txt
```

---

## 📌 Ghi chú
- Cổng `8000`: dành cho WebSocket hoặc API chung.
- Cổng `8001`: dành riêng cho Chatbot (nếu chạy tách).
- Cần chắc chắn `llama3` đã chạy bằng Ollama trước khi gọi API Chatbot.

---
