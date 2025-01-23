from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from kafka import KafkaConsumer

# Parametri Kafka
KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC = 'report'

# Parametri InfluxDB
token = "kMT5DBlHJYptEdfv47xSk3bGD5aO7IDQubrsHgjulScT0Hw_-1kOkfQMyWPrZdR_Dnz5p-Y3TS7zDLI6CbBOUw=="
org = "influxdb"
bucket = "influxdb"
client = InfluxDBClient(url="http://influxdb:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Configurazione del consumer Kafka
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER, auto_offset_reset='earliest', group_id='consumer-group')

# Consumo dei messaggi da Kafka e invio a InfluxDB
for message in consumer:
    # Decodifica il messaggio in formato JSON
    data = json.loads(message.value.decode('utf-8'))

    # Creazione del punto InfluxDB
    point = Point("plant_data") \
        .tag("plant_id", data['plant_id']) \
        .field("temperature", float(data['temperature'])) \
        .field("humidity", float(data['humidity'])) \
        .field("luminosity", float(data['luminosity'])) \
        .field("timestamp", data['timestamp'])

    # Scrittura del punto su InfluxDB
    try:
        write_api.write(bucket, org, point)
        print(f"Data sent to InfluxDB: {data}")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

