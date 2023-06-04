#!/usr/bin/env python

import argparse
from typing import Optional
import time

from google.cloud import pubsub_v1
import paho.mqtt.client as mqtt

fruitList = []

project_id = 'second-core-387205'
ready_id = 'ready-sub'
pub_id = 'fruit-list'
gpt_id = 'chat-gpt'

broker_hostname = "student1-desktop.local"
broker_port = 1883
broker_username = "FruitDetector1"
broker_password = "123"

FruitTopic = "Fruit_Topic"
readyTopic = "Ready_Topic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker")

def on_publish(client, userdata, mid):
    print("Message published")

def on_message(client, userdata, msg):
    global fruitList
    fruitStr=""
    print(f"Received message: {msg.payload.decode()}")
    if msg.payload.decode('utf-8') == '53':
        fruitList.append('Apple')
    elif msg.payload.decode('utf-8') == '52':
        fruitList.append('Banana')
    elif msg.payload.decode('utf-8') == "done":
        for i in range(len(fruitList)):
            if i == 0:
                fruitStr += fruitList[i]
            else:
                fruitStr += ' and ' + fruitList[i]
        pub(project_id, pub_id, fruitStr)
        fruitStr=""
        fruitList.clear()

            

           
    print(fruitList)



client = mqtt.Client()

client.username_pw_set(broker_username, broker_password)

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish


client.connect(broker_hostname, broker_port, 60)



client.loop_start()

def sub(project_id: str, subscription_id: str, timeout: Optional[float] = None) -> None:

    subscriber_client = pubsub_v1.SubscriberClient()

    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
    
        message.ack()
        print(f"Acknowledged {message.message_id}.")
        if message.data.decode('utf-8') == 'Ready':
            print("Received 'Ready', subscribing to MQTT topic.")
            client.subscribe(FruitTopic)
            client.publish(readyTopic, "Ready For Fruit")

            
    
    streaming_pull_future = subscriber_client.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    try:
    
        streaming_pull_future.result(timeout=timeout)
    except:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    subscriber_client.close()

def pub(project_id: str, topic_id: str, messageR) -> None:
    client = pubsub_v1.PublisherClient()

    topic_path = client.topic_path(project_id, topic_id)

    data = bytes(messageR, 'utf-8')


    api_future = client.publish(topic_path, data)
    message_id = api_future.result()

    print(f"Published {data.decode()} to {topic_path}: {message_id}")


if __name__ == "__main__":
    
    sub(project_id, ready_id)

