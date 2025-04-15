# pbl5_Flood_warning_system
Đồ án KTMT

// Chạy server bằng môi trường ảo
- Mở CMD tại \PBL5_Flood_warning_system
- python -m venv venv
- Nhập venv\Scripts\activate (trên window)
- python install -r requirements.txt
- Nhập cd be

<!-- Chạy lệnh: uvicorn main:app --reload --host 0.0.0.0 --port 8000 -->

Chaỵ lệnh uvicorn app.main:app --reload
Fake dữ liệu: mở terminal trên \PBL5_Flood_warning_system. Chạy lệnh: python fake_data.py