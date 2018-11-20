

############################################################################################
#
#   GCP Pub/Sub Functions
#
#   References:
#   https://cloud.google.com/pubsub/docs/
#
############################################################################################


import sys, os
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dzaratsian/gcpkey.json"


############################################################################################
#
#   Functions
#
############################################################################################


def pubsub_create_topic(project_id, topic_name):
    '''
        Create Google Pub/Sub Topic

    '''
    try:
        publisher   = pubsub_v1.PublisherClient()
        topic_path  = publisher.topic_path(project_id, topic_name)
        topic       = publisher.create_topic(topic_path)
        print('[ INFO ] Topic created: projects/{}/topics/{}'.format(project_id, topic_name))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_delete_topic(project_id, topic_name):
    '''
        Delete Google Pub/Sub Topic

        Notes:
          - When you delete a topic, its subscriptions are not deleted.
          - A subscription's message backlog will still be available for subscribers.
          - After a topic is deleted, its subscriptions have the topic name _deleted-topic_

    '''
    try:
        publisher   = pubsub_v1.PublisherClient()
        topic_path  = publisher.topic_path(project_id, topic_name)
        topic       = publisher.delete_topic(topic_path)
        print('[ INFO ] Topic deleted: {}'.format(topic_name))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_list_topics(project_id):
    '''
        List all Topics within a Project

        Notes:
          - By default, a maximum of 100 results are returned per query.
          - You can specify an alternative value up to 1,000 using the page size parameter.

    '''
    try:
        publisher    = pubsub_v1.PublisherClient()
        project_path = publisher.project_path(project_id)
        print('[ INFO ] Pub/Sub Topics within GCP Project {}'.format(project_id))
        for i, topic in enumerate(publisher.list_topics(project_path)):
            print('     Topic {}:\t{}'.format(i, topic.name))
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_pull_subscription(project_id, topic_name, subscription_name):
    '''
        Creates a Pull Subscription

        Notes:
          - Must create a subscription to a topic before subscribers can receive messages published to the topic.
          - Use the Cloud Pub/Sub GCP Console (or CLI) to change the subscription type (to Pull or Push).
                - To convert a push subscription to pull, change the URL to an empty string.
                - To convert a pull subscription to push, set a valid URL.

    '''
    try:
        subscriber        = pubsub_v1.SubscriberClient()
        topic_path        = subscriber.topic_path(project_id, topic_name)
        subscription_path = subscriber.subscription_path(project_id, subscription_name)
        subscription      = subscriber.create_subscription(subscription_path, topic_path)
        
        print('[ INFO ] Subscription created: {}'.format(subscription.name))
        print({
            'name':                 subscription.name,
            'topic':                subscription.topic,
            'ack_deadline_seconds': subscription.ack_deadline_seconds,
            'message_retention':    subscription.message_retention_duration.seconds
        })
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_push_subscription(project_id, topic_name, subscription_name):
    '''
        Creates a Push Subscription

        Notes:
          - Must create a subscription to a topic before subscribers can receive messages published to the topic.
          - Use the Cloud Pub/Sub GCP Console (or CLI) to change the subscription type (to Pull or Push).
                - To convert a push subscription to pull, change the URL to an empty string.
                - To convert a pull subscription to push, set a valid URL.

    '''
    try:
        subscriber        = pubsub_v1.SubscriberClient()
        topic_path        = subscriber.topic_path(project_id, topic_name)
        subscription_path = subscriber.subscription_path(project_id, subscription_name)
        
        push_config  = pubsub_v1.types.PushConfig(push_endpoint=endpoint)
        subscription = subscriber.create_subscription(subscription_path, topic_path, push_config)
        
        print('[ INFO ] Push subscription created: {}'.format(subscription))
        print('[ INFO ] Endpoint for subscription is: {}'.format(endpoint))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_list_subscriptions(project_id):
    '''
        List Google Pub/Sub Subscriptions
    
    '''
    try:
        subscriber   = pubsub_v1.SubscriberClient()
        project_path = subscriber.project_path(project_id)
        
        print('[ INFO ] Pub/Sub Subscriptions within GCP Project {}'.format(project_id))
        for i, subscription in enumerate(subscriber.list_subscriptions(project_path)):
            print('')
            print('\tSubscription Name:        {}'.format(subscription.name))
            print('\tSubscription Topic:       {}'.format(subscription.topic))
            print('\tAck Deadline (secs):      {}'.format(subscription.ack_deadline_seconds))
            print('\tMessage Retention (secs): {}'.format(subscription.message_retention_duration.seconds))
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_delete_subscription(project_id, subscription_name):
    '''
        Delete Google Pub/Sub Subscription

    '''
    try:
        subscriber        = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_name)
        
        subscriber.delete_subscription(subscription_path)
        
        print('Subscription deleted: {}'.format(subscription_path))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))































def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print(message_future.result())



def pubsub_publish(project_id, topic_name, message):
    '''
        Publish data to Google Pub/Sub
        
        USAGE:
        pubsub_publish(project_id='zproject201807', topic_name='ztopic1', message='test message 1')
        
        Concepts:
            - At-least-once message delivery
            - Does not handle or care about out of order message (these are handled in Dataflow)
            - Data / message must be base64-encoded
            - Messages must be smaller than 10MB (after decoding)
            - Note that the message payload must not be empty.
            - Asynchronous publishing allows for batching and higher throughput in your application.
        
    '''
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    
    message = message.encode('utf-8')
    message_future = publisher.publish(topic_path, data=message)
    message_future.add_done_callback(callback)



if __name__ == "__main__":
    
    if len(sys.argv) == 4:
            project_id        = sys.argv[1]
            topic_name        = sys.argv[2]
            subscription_name = sys.argv[3]
    else:
        print('[ Usage ] pubsub_subscriber.py <project_id> <topic_name> <subscriber_name>')
        sys.exit()
    
    gcp_pubsub_subscribe(project_id, topic_name, subscription_name)



#ZEND
