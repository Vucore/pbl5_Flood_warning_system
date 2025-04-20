# from influxdb_client import InfluxDBClient, Point, WriteOptions
# from app import config  # Import cấu hình từ config.py
# from SensorData import SensorData

# # Tạo client kết nối đến InfluxDB
# client = InfluxDBClient(url=config.INFLUXDB_URL, token=config.INFLUXDB_TOKEN, org=config.INFLUXDB_ORG)
# write_api = client.write_api(write_options=WriteOptions(batch_size=1))

# # Hàm ghi dữ liệu vào InfluxDB
# def save_sensor_data(sensor: SensorData):
#     point = (
#         Point("sensor_data")
#         .field("rainfall", (float)(sensor.rainfall))
#         .field("water_level", (float)(sensor.water_level))
#         .field("soil_humidity", (float)(sensor.soil_humidity))
#         .field("air_humidity", (float)(sensor.air_humidity))
#         .field("air_pressure", (float)(sensor.air_pressure))
#         .field("temperature", (float)(sensor.temperature))
#     )
#     write_api.write(bucket=config.INFLUXDB_BUCKET, org=config.INFLUXDB_ORG, record=point)
#     return {"message": "Data saved successfully"}

# # Hàm lấy dữ liệu mới nhất
# def get_latest_data():
#     query_api = client.query_api()
#     query = f'''
#         from(bucket: "{config.INFLUXDB_BUCKET}")
#         |> range(start: {config.QUERY_RANGE})  
#         |> filter(fn: (r) => r._measurement == "sensor_data")
#         |> sort(columns: ["_time"], desc: true)
#         |> limit(n: 1)
#     '''
#     result = query_api.query(org=config.INFLUXDB_ORG, query=query)
    
#     if result and result[0].records:
#         data = {
#             "time": result[0].records[0].get_time(),
#             "rainfall": None,
#             "soil_humidity": None,
#             "air_humidity": None,
#             "air_pressure": None,
#             "temperature": None,
#             "water_level": None
#         }
#         for record in result[0].records:
#             if record.get_field() in data:
#                 data[record.get_field()] = record.get_value()
#         return data
#     return {"message": "No data found"}
