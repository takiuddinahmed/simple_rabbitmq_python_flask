
from multiprocessing import connection
import pika
from flask import Flask, request
from dotenv import load_dotenv
import os 
load_dotenv()

connection_url = os.environ.get('connection_url')

def publish_msg(msg):
    print(f" [x] Sending '{msg}'")
    connection = pika.BlockingConnection(pika.URLParameters(connection_url))

    channel = connection.channel()

    channel.queue_declare(queue='message')

    channel.basic_publish(exchange='', routing_key='message', body=msg)
    print(f" [x] Sent '{msg}'")
    connection.close()


app = Flask(__name__)

@app.route('/')
def index_route():
    return 'OK! it works'


@app.route('/message',methods=['POST'])
def message_route():
    json = request.get_json()
    msg = json['msg']
    publish_msg(msg)
    return msg;


if __name__ == '__main__':
    app.run(debug=True)