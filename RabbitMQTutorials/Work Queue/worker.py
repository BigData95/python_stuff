import os
import sys
import time

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(10)
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    # Fair Dispatch
    channel.basic_qos(prefetch_count=1)    
    # Tenemos que decirle que consume de la cola hello
    channel.basic_consume(queue='task_queue',
                          on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
