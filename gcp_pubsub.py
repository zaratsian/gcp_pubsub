

############################################################################################
#
#   GCP PubSub Publisher
#
#   References:
#   https://cloud.google.com/pubsub/docs/
#
#   Usage:  gcp_pubsub_publisher.py <project_id> <topic_name> <subscriber_name>
#
############################################################################################



import sys,os
import logging
import multiprocessing
import random
import time
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dzaratsian/key.json"


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










def pubsub_publish(project_id, topic_name, message):
    '''
        Pub/Sub Publish Message

        Notes:
          - When using JSON over REST, message data must be base64-encoded
          - Messages must be smaller than 10MB (after decoding)
          - The message payload must not be empty
          - Attributes can also be added to the publisher payload
    
    '''
    try:
        publisher  = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)
        
        def callback(message_future):
            # When timeout is unspecified, the exception method waits indefinitely.
            if message_future.exception(timeout=30):
                print('[ ERROR ] Publishing message on {} threw an Exception {}.'.format(topic_name, message_future.exception()))
            else:
                print('[ INFO ] Result: {}'.format(message_future.result()))
        
        # When you publish a message, the client returns a Future.
        # Att
        message_future = publisher.publish(topic_path, data=message.encode('utf-8'), attribute1='myattr1', anotherattr='myattr2')
        message_future.add_done_callback(callback)
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_subscribe_async(project_id, subscription_name):
    '''
        Pub/Sub Subscribe - Asynchronous PULL

        Notes:
          - Asynchronous pulling provides higher throughput
          - Does not requiring your application to block for new messages
          - Messages can be received in app using a long running message listener, and acknowledged one message at a time.
          - Message Flow Control
                - The need for flow control indicates that messages are being published at a higher rate than they are being consumed
                - Your subscriber client might process and acknowledge messages slower than Cloud Pub/Sub sends them to the client. 
                - This could lead to out of memory issues
                - To handle this, use the flow control features of the subscriber to control the rate at which the subscriber retrieves messages.
                    ie. flow_control = pubsub_v1.types.FlowControl(max_messages=10)
                        subscriber.subscribe(subscription_path, callback=callback, flow_control=flow_control)
    
    '''
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_name)
        
        def callback(message):
            
            # Process pubsub message
            print('Received message: {}'.format(message.data))
            # ... do something with message.data (actual message), such as write to dataflow, persist in db, etc ...
            
            # Processing Custom Attributes
            if message.attributes:
                # ... do something with message.attributes ...
                print('Attributes:')
                for key in message.attributes:
                    value = message.attributes.get(key)
                    print('{}: {}'.format(key, value))
            
            message.ack()
        
        subscriber.subscribe(subscription_path, callback=callback)
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def pubsub_subscribe_sync(project_id, subscription_name, num_messages=1):
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





#ZEND
