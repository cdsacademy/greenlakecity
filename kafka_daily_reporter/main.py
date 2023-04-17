from kafka import KafkaProducer
from datetime import datetime, timedelta
import json
import time
import os

DATA_DIRECTORY = '/app/data'
KAFKA_SERVERS = f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"
START_DATE = datetime.strptime(os.environ.get('START_DATE'), '%d/%m/%Y')
END_DATE = datetime.strptime(os.environ.get('END_DATE'), '%d/%m/%Y')

time.sleep(20)

datasets = {}

for filename in os.listdir(DATA_DIRECTORY):
    with open(f"{DATA_DIRECTORY}/{filename}", 'r') as f:
        data = json.load(f)
    datasets[os.path.splitext(filename)[0]] = data

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVERS)
current_date = START_DATE
while current_date <= END_DATE:
    str_current_date = current_date.strftime('%d/%m/%Y')
    print(str_current_date)
    for topic, dataset in datasets.items():
        message = json.dumps({str_current_date: dataset[str_current_date]})
        producer.send(topic, message.encode('utf-8'))
    time.sleep(3)
    current_date += timedelta(days=1)

# kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic hydrodataWAT001 --from-beginning

# kafka-topics.sh --bootstrap-server kafka:9092 --list