import openai
from google.cloud import pubsub

# openai.api_key = ''
    # chat gpt API key removed
messages = [{"role": "system", "content": "You are an intelligent assistant."}]

messageSent = False

def message_handler(message):
   
    fruitStr = message.data.decode('utf-8')
    messageINPUT = f'If I have an {fruitStr}, what dishes can I make? Can you give me recipes and a shopping list for each recipe?'
    pub_message = f'User: {messageINPUT}\n'
    
    message.ack()

    if messageINPUT:
        messages.append({"role": "user", "content": messageINPUT})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})

        pub_message += f'ChatGPT: {reply}'
        pub_message = bytes(pub_message, 'utf-8')
        pub(pub_message) # sends chat gpt output to user terminal

def listen_for_messages(project_id, subscription_id):
    subscriber = pubsub.SubscriberClient()

    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        message_handler(message)

    subscriber.subscribe(subscription_path, callback=callback)

    print(f"Listening for messages on {subscription_path}...")

    while not messageSent:
        pass

def pub(message_data):
    global messageSent
    messageSent = True
    publisher = pubsub.PublisherClient()
    topic_name = 'projects/second-core-387205/topics/chat-gpt'

    # Convert message_data to bytes if it's not already in bytes
    if not isinstance(message_data, bytes):
        message_data = message_data.encode('utf-8')
    future = publisher.publish(topic_name, message_data)
    result = future.result()
    print(f"Message published: {result}")

project_id = 'second-core-387205'
subscription_id = 'fruit-list-sub'

listen_for_messages(project_id, subscription_id)
