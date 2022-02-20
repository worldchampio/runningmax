import pika
import json
import sys

def on_message_received(ch, method, properties, body):
    print(json.loads(body))
try:
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs', 
                            exchange_type='topic')
    routing_key = 'solution'

    queue = channel.queue_declare(queue='', 
                                exclusive=True)

    channel.queue_bind(exchange='topic_logs',
                    routing_key=routing_key,
                    queue=queue.method.queue)

    channel.basic_consume(queue=queue.method.queue,
                        auto_ack=True,
                        on_message_callback=on_message_received)

    print("Started listening on %r" % routing_key)
    channel.start_consuming()
except KeyboardInterrupt:
    print("Stopping")
    channel.stop_consuming()
    connection.close()
