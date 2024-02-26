import json
from google.cloud import pubsub_v1
from google.cloud import firestore
import sys

subscription_name = "cantiere_sub"
project_id = "cmgeneralsac"

subscriber=pubsub_v1.SubscriberClient()

subscription_path=subscriber.subscription_path(project_id, subscription_name)
print(subscription_path)

db = firestore.Client()

cap1 = sys.argv[1]


def callback(message):

    if json.loads(message.data)['cap'] == int(cap1):
        print(f'message received: {message.data}')
        message.ack()

if __name__=='__main__':
    pull = subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result(timeout=20)
    except:
        pull.cancel()