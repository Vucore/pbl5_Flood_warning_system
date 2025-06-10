from collections import deque
from ...data_module.database.db import DataRain
from datetime import datetime, timedelta

# Khởi tạo danh sách lưu trữ 360 mẫu gần nhất
rain_duration = 0
MAX_HOURS = 168
SAMPLES_PER_HOUR = 60
hourly_rainfall = deque(maxlen=MAX_HOURS)  # Lưu tổng lượng mưa của mỗi giờ, tối đa 168 giờ
# Khởi tạo danh sách lưu dữ liệu lượng mưa trong giờ hiện tại
current_hour_rainfall = deque(maxlen=SAMPLES_PER_HOUR)  # Lưu lượng mưa của giờ hiện tại
last_hour = None
dr = DataRain("storage/datarain.db")
dr.create_table_rain()

def init_hourly_rainfall():
    """
    Hàm khởi tạo danh sách hourly_rainfall từ database.
    Lấy dữ liệu lượng mưa của 168 giờ gần nhất và chuyển đổi thành danh sách giá trị lượng mưa.
    """
    current_time = datetime.now()
    start_time = current_time - timedelta(hours=168)
    start_timestamp = start_time.strftime("%Y-%m-%d %H:%M:%S")

    # Lấy dữ liệu từ database
    result = dr.get_rainfall_data_from_timestamp(timestamp=start_timestamp)

    if result["success"]:
        # Chuyển đổi dữ liệu thành danh sách lượng mưa
        rainfall_values = [data["rainfall"] for data in result["data"]]
        return deque(rainfall_values, maxlen=MAX_HOURS)
    else:
        print("Lỗi khi khởi tạo hourly_rainfall:", result["message"])
        return deque(maxlen=MAX_HOURS)  # Trả về danh sách rỗng nếu có lỗi

hourly_rainfall = init_hourly_rainfall()

def add_sensor_rainfall(rainfall):
    """
    Hàm thêm dữ liệu cảm biến vào danh sách.
    Nếu danh sách vượt quá 60 mẫu, mẫu cũ nhất sẽ tự động bị xóa.
    """
    current_hour_rainfall.append(rainfall)

def get_latest_rainfall():
    """
    Hàm lấy toàn bộ dữ liệu hiện tại trong danh sách.
    """
    return list(current_hour_rainfall)

def calculate_average_rainfall(list_rainfall):
    """
    Hàm tính trung bình lượng mưa trong 60 mẫu gần nhất.
    """
    if len(list_rainfall) == 0:
        return 0  # Trả về 0 nếu danh sách rỗng
    return sum(list_rainfall) / len(list_rainfall)

def shift_hour():
    """
    Hàm chuyển sang giờ mới.
    Tính tổng lượng mưa của giờ hiện tại, lưu vào danh sách hourly_rainfall_totals,
    và reset dữ liệu cho giờ mới.
    """
    avg_rainfall = calculate_average_rainfall(current_hour_rainfall)
    hourly_rainfall.append(avg_rainfall)
    current_hour_rainfall.clear()


    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    dr.insert_rainfall_data(rainfall=avg_rainfall, timestamp=timestamp)

def add_hourly_rainfall(rainfall):
    """
    Hàm thêm dữ liệu trung bình 1 giờ vào danh sách.
    Nếu danh sách vượt quá 168 mẫu, mẫu cũ nhất sẽ tự động bị xóa.
    """
    hourly_rainfall.append(rainfall)

def get_latest_hourly_rainfall(hours=24):
    """
    Hàm lấy dữ liệu lượng mưa của các giờ gần nhất.
    :param hours: Số giờ cần lấy (mặc định là 24 giờ).
    :return: Danh sách lượng mưa của các giờ gần nhất hoặc toàn bộ nếu số giờ vượt quá danh sách.
    """
    if hours > len(hourly_rainfall):
        # print(f"Chỉ có {len(hourly_rainfall)} giờ trong danh sách, trả về toàn bộ.")
        return list(hourly_rainfall)
    return list(hourly_rainfall)[-hours:]  # Lấy danh sách từ cuối lên theo số giờ yêu cầu

def control_prepare_data_rainfall(rainfall):
    """
    Hàm điều khiển toàn bộ các hàm trong file prepare_data.py.
    :param sensor_data: Dữ liệu cảm biến (lượng mưa theo mẫu).
    :param hours_to_get: Số giờ cần lấy dữ liệu lượng mưa (mặc định là 24 giờ).
    :return: Danh sách lượng mưa của các giờ gần nhất.
    """
    global rain_duration, last_hour

    # Lấy giờ hiện tại
    current_time = datetime.now()
    current_hour = current_time.hour

    # Kiểm tra nếu đã qua giờ mới
    if last_hour is not None and current_hour != last_hour:
        shift_hour()

    # Cập nhật giờ cuối cùng
    last_hour = current_hour

    # Thêm dữ liệu cảm biến vào giờ hiện tại
    add_sensor_rainfall(rainfall=rainfall)

    # Tính các đặc trưng lượng mưa
    rain_24h_data = get_latest_hourly_rainfall(hours=24)  # Lấy danh sách lượng mưa trong 24 giờ gần nhất
    rain_48h_data = get_latest_hourly_rainfall(hours=48)  # Lấy danh sách lượng mưa trong 48 giờ gần nhất
    rain_168h_data = get_latest_hourly_rainfall(hours=168)  # Lấy danh sách lượng mưa trong 168 giờ gần nhất

    rain_24h = sum(rain_24h_data)  # Tổng lượng mưa trong 24 giờ gần nhất
    rain_48h_avg = sum(rain_48h_data) / len(rain_48h_data) if len(rain_48h_data) > 0 else 0  # Trung bình lượng mưa trong 48 giờ
    rain_max_24h = max(rain_24h_data) if len(rain_24h_data) > 0 else 0  # Lượng mưa lớn nhất trong 24 giờ, trả về 0 nếu danh sách rỗng
    rain_acc_week = sum(rain_168h_data)  # Tổng lượng mưa trong 7 ngày (168 giờ)
    
    # Cập nhật giá trị rain_duration
    if rain_48h_avg > 0.025:
        rain_duration += 1  # Tăng lên 1 nếu trung bình lượng mưa > 0.025
    elif rain_48h_avg < 0.025:
        rain_duration = 0  # Đặt bằng 0 nếu trung bình lượng mưa < 0.025

    return {
        "rain_duration": rain_duration,
        "rain_24h": rain_24h,
        "rain_48h_avg": rain_48h_avg,
        "rain_max_24h": rain_max_24h,
        "rain_acc_week": rain_acc_week
    }