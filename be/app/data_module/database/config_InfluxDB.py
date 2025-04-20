import os
# Cấu hình kết nối đến InfluxDB
INFLUXDB_URL = "http://localhost:8086"  
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")  
INFLUXDB_ORG = "Miserable people"
INFLUXDB_BUCKET = "PBL5"

# Cấu hình truy vấn dữ liệu
QUERY_RANGE = "-1h"  # Lấy dữ liệu trong vòng 1 giờ qua
