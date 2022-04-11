
import pika

from dotenv import load_dotenv
import os 
load_dotenv()

connection_url = os.environ.get('connection_url')




def got_msg(ch, method, properties, body):
    print(" [x] Received %r" % body)

def main():
    connection = pika.BlockingConnection(pika.URLParameters(connection_url))

    channel = connection.channel()

    channel.queue_declare(queue="message")

    channel.basic_consume(
        queue="message",
        auto_ack=True,
        on_message_callback=got_msg
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
