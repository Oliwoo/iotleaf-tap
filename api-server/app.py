from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from influxdb_client import InfluxDBClient, QueryApi
import json

app = Flask(__name__)

# Configurazione
KAFKA_BROKER = "kafka:9092"
INFLUX_URL = "http://influxdb:8086"
INFLUX_TOKEN = "password"
INFLUX_ORG = "org"
INFLUX_BUCKET = "irrigation"

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# InfluxDB Client
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = influx_client.query_api()

@app.route("/register", methods=["POST"])
def register_device():
    device_id = request.json.get("device_id")
    if not device_id:
        return jsonify({"error": "Device ID is required"}), 400

    # Aggiungere il dispositivo a un elenco interno o logica di registrazione
    message = {"event": "register", "device_id": device_id}
    producer.send("device-events", message)
    return jsonify({"message": f"Device {device_id} registered successfully!"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    query = f'from(bucket:"{INFLUX_BUCKET}") |> range(start: -1h)'
    tables = query_api.query(query)
    data = []
    for table in tables:
        for record in table.records:
            data.append({"time": record.get_time(), "value": record.get_value()})
    return jsonify(data)

@app.route("/command", methods=["POST"])
def send_command():
    device_id = request.json.get("device_id")
    command = request.json.get("command")
    if not device_id or not command:
        return jsonify({"error": "Device ID and command are required"}), 400

    message = {"device_id": device_id, "command": command}
    producer.send("device-commands", message)
    return jsonify({"message": f"Command sent to {device_id}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
