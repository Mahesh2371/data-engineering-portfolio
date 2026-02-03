from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode()
)

while True:
    data = {"user": random.randint(1,100), "amount": random.randint(100,1000)}
    producer.send("transactions", data)
    print("Sent:", data)
    time.sleep(1)
