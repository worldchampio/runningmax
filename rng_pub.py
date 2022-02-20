from random import randint
import pika
import json
from time import sleep

def make_rng():
    return randint(0,10)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
routing_key = 'rand'

for i in range(0,1000):
    message = {
        "sequence_number" : int(i),
        "rand" : int(make_rng())
    }
    sleep(0.01)
    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=json.dumps(message))
    #print("Sent %r:%r" % (routing_key, json.dumps(message)))
connection.close()