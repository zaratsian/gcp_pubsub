

###################################################################################################
#
#   GCP PubSub Subscriber (Synchronous)
#
#   References:
#   https://cloud.google.com/pubsub/docs/
#
#   USAGE:  gcp_pubsub_subscribe_sync.py project_id subscription_name <num_messages>
#
###################################################################################################


import sys, os
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dzaratsian/gcpkey.json"


###################################################################################################
#
#   Functions
#
###################################################################################################


def pubsub_subscribe_sync(project_id, subscription_name, num_messages=1, ack_deadline=30, sleep_time=10):
    '''
        Pub/Sub Subscribe - Synchronous PULL
        Notes:
          - Synchronous pull is better suited to workloads that do not require handling of messages as soon as they are published.
          - Does not need to keep a long-running connection alive
          - Can choose to pull and handle a fixed number of messages
          - The subscriber times out if no messages are currently available to be handled.
          - For low latency, it's important to have many simultaneously outstanding pull requests with returnImmediately = false
          - It's typical to have 10-100 requests outstanding at a time
    '''
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_name)
        
        response = subscriber.pull(subscription_path, max_messages=num_messages)

        print('[ INFO ] Received {} messages'.format(len(response.received_messages)))
        
        for msg in response.received_messages:
            # ... do something with msg ... #
            print({'id':msg.message.message_id, 'message':msg.message.data})
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



###################################################################################################
#
#   Main
#
###################################################################################################

if __name__ == "__main__":
    
    if len(sys.argv) >= 3:
            project_id        = sys.argv[1]
            subscription_name = sys.argv[2]
    else:
        print('[ Usage ] gcp_pubsub_subscribe_sync.py project_id subscription_name <num_messages>')
        sys.exit()
    
    pubsub_subscribe_sync(project_id, subscription_name, num_messages=1)



#ZEND
