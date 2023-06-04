
# This code sends a 
# with code used from google's github @ https://github.com/googleapis/python-pubsub/blob/3ffb93602538fc912bcbe0c24f0f4c5d5311fac0/samples/snippets/subscriber.py


from typing import Optional

from google.cloud import pubsub_v1

def sub(project_id: str, subscription_id: str, timeout: Optional[float] = None) -> None:
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull]
    # [START pubsub_quickstart_subscriber]


    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    #this is the HANDLER for the message 
    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message.data.decode()}.")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first. 
            # streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscriber_async_pull]
    # [END pubsub_quickstart_subscriber]

def pub(project_id: str, topic_id: str, message) -> None:
publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

data_str = message
# Data must be a bytestring
data = data_str.encode("utf-8")
# When you publish a message, the client returns a future.
future = publisher.publish(topic_path, data)
print(future.result())

print(f"Published {data.decode()} to {topic_path}: {message_id}")


if __name__ == "__main__":

    # project_id = 'second-core-387205'
    # project_id = 'nimble-radio-387221'
    ready_topic = 'ready'
    
    #sub_chat = 'chat-gpt-sub'
    sub_chat. = 'my_sub'

    pub(project_id, ready_topic, 'Ready')
    
    sub(project_id, sub_chat)
