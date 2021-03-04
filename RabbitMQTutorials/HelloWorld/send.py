import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


# Es buena pratica declarar la cola de nuevo
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello!!!')
print("[x] sent 'Hello nigg!'")

connection.close()
