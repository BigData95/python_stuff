import sys

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

# Publishing to a non-existing exchange is forbidden.
# Declara Exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Emit log"
channel.basic_publish(exchange='logs', routing_key='', body=message)

print("[x] Sent %r" %message)
connection.close()
