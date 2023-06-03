from typing import Optional

from google.cloud import pubsub_v1

def sub(project_id: str, subscription_id: str, timeout: Optional[float] = None) -> None:
    """Receives messages from a Pub/Sub subscription."""
    # Initialize a Subscriber client
    subscriber_client = pubsub_v1.SubscriberClient()
    # Create a fully qualified identifier in the form of
    # `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received\n{message.data.decode()}.")
        # Acknowledge the message. Unack'ed messages will be redelivered.
        message.ack()
        print(f"Acknowledged {message.message_id}.")
        stopsub(streaming_pull_future)

    def stopsub(streaming_pull_future):
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

    streaming_pull_future = subscriber_client.subscribe(
        subscription_path, callback=callback
    )
    print(f"Listening for messages on {subscription_path}..\n")

    streaming_pull_future.result(timeout=timeout)

    subscriber_client.close()

def pub(project_id: str, topic_id: str, message) -> None:
    """Publishes a message to a Pub/Sub topic."""
    # Initialize a Publisher client.
    client = pubsub_v1.PublisherClient()
    # Create a fully qualified identifier of form `projects/{project_id}/topics/{topic_id}`
    topic_path = client.topic_path(project_id, topic_id)

    # Data sent to Cloud Pub/Sub must be a bytestring.
    data = bytes(message, 'utf-8')

    # When you publish a message, the client returns a future.
    api_future = client.publish(topic_path, data)
    message_id = api_future.result()

    print(f"Published {data.decode()} to {topic_path}: {message_id}")


if __name__ == "__main__":

    project_id = 'second-core-387205'
    ready_topic = 'ready'
    sub_chat = 'chat-gpt-sub'

    pub(project_id, ready_topic, 'Ready')
    
    sub(project_id, sub_chat)
