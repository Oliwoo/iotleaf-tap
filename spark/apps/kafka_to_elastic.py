from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Crea una sessione Spark
spark = SparkSession.builder \
    .appName("KafkaToElasticsearch") \
    .getOrCreate()

# Leggi i dati dal topic Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "report") \
    .load()

# Decodifica il messaggio Kafka (presupponendo che il valore sia in formato JSON)
kafka_df = kafka_df.selectExpr("CAST(value AS STRING)").alias("json_data")
kafka_df = kafka_df.selectExpr("json_data", "json_data->'plant_id' AS plant_id", 
                               "json_data->'temperature' AS temperature", 
                               "json_data->'humidity' AS humidity", 
                               "json_data->'luminosity' AS luminosity", 
                               "json_data->'timestamp' AS timestamp")

# Scrivi i dati su Elasticsearch
kafka_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "elasticsearch:9200") \
    .option("es.resource", "sensor_data/_doc") \
    .option("es.index.auto.create", "true") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
