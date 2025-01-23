# Usa un'immagine Python come base
FROM python:3.9-bullseye

USER root
# Installa Java, procps e altre dipendenze necessarie
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk-headless \
    procps \
    wget \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Imposta JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
ENV SPARK_PACKAGES=org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia lo script Python nel container
COPY ./apps/kafka_to_elastic.py kafka_to_elastic.py

# Comando per eseguire lo script
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0", "/kafka_to_elastic.py"]