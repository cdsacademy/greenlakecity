from kafka import KafkaProducer
import json
import time
import os

DATA_DIRECTORY = '/app/data'
KAFKA_SERVERS = f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"

time.sleep(20)

datasets = {}

for filename in os.listdir(DATA_DIRECTORY):
    with open(f"{DATA_DIRECTORY}/{filename}", 'r') as f:
        data = json.load(f)
    datasets[os.path.splitext(filename)[0]] = data

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVERS)
for topic, dataset in datasets.items():
    for date in dataset:
        message = json.dumps({date: dataset[date]})
        producer.send(topic, message.encode('utf-8'))
        time.sleep(3)

# kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic weather --from-beginning

# kafka-topics.sh --bootstrap-server kafka:9092 --list