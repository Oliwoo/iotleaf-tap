from kafka import KafkaConsumer
import paho.mqtt.publish as mqtt_publish
import json

# Configurazioni
KAFKA_BROKER = "kafka:9092"
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883

# Simulazione delle configurazioni delle piante
PLANT_CONFIGS = {
    "token_1": {"device_id": "device_1", "threshold": 30},  # Threshold di esempio per l'irrigazione
    "token_2": {"device_id": "device_2", "threshold": 25},
}

def process_message(message):
    try:
        data = json.loads(message.value.decode("utf-8"))
        token = data.get("token")
        moisture_level = data.get("moisture_level")

        if not token or token not in PLANT_CONFIGS:
            print(f"Ignorando messaggio non valido o token sconosciuto: {data}")
            return

        config = PLANT_CONFIGS[token]
        device_id = config["device_id"]
        threshold = config["threshold"]

        # Verifica se inviare il comando di irrigazione
        if moisture_level < threshold:
            command = {"action": "irrigate"}
            mqtt_publish.single(
                topic=f"doAction/{device_id}",
                payload=json.dumps(command),
                hostname=MQTT_BROKER,
                port=MQTT_PORT,
            )
            print(f"Comando inviato a {device_id}: {command}")
        else:
            print(f"Condizioni ottimali per {device_id}, nessun comando inviato.")

    except Exception as e:
        print(f"Errore nel processamento del messaggio: {e}")

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "plant-data",
        bootstrap_servers=KAFKA_BROKER,
        group_id="data-processor-group",
        auto_offset_reset="earliest",
    )
    print("In ascolto dei messaggi su Kafka...")
    for message in consumer:
        process_message(message)
