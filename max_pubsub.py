import time
import pika
import numpy as np
import json
from collections import deque

reconnect_on_failure = True
randholder = deque([], maxlen=10)

def consumer(connection, channel):
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    result = channel.queue_declare(queue='original_queue', exclusive=True)
    channel.queue_bind(exchange='topic_logs',routing_key='rand' ,queue=result.method.queue)
    print(' [*] Waiting for messages from \'rand\'. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        # Load the json body to parse it
        body_pub = json.loads(body)
        randholder.append(body_pub['rand'])

        rmax = max(randholder)

        out = {
            "sequence_number" : int(body_pub["sequence_number"]),
            "rand" : int(body_pub["rand"]),
            "running_max" : int(rmax)
        }
        
        ch.basic_publish(exchange='topic_logs', routing_key='solution', body=json.dumps(out))

    channel.basic_consume(
        queue='original_queue', 
        on_message_callback=callback, 
        auto_ack=True)

    channel.start_consuming()

def get_connection_and_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    return connection, channel

def start(reconnect_on_failure):
    connection, channel = get_connection_and_channel()
    consumer(connection, channel)
    # the if condition will be executed when the consumer's start_consuming loop exists
    if reconnect_on_failure:
        # cleanly close the connection and channel
        if not connection.is_closed():
            connection.close()
        if not channel.is_close():
            channel.close()
        start(reconnect_on_failure)

start(reconnect_on_failure)