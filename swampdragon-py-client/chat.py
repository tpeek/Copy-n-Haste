#!/usr/bin/env python
from sdclient import DragonClient


# Print every new message and the sender
def on_channel_message(channel, message):
    output = '{} says: {}'.format(message.get('name'), message.get('message'))
    print(output)


# Joined the chat
def on_subscribed(context, message):
    print('-you joined the chat-')
    print('Chat away...')


if __name__ == '__main__':
    url = 'ws://localhost:9999/data'
    client = DragonClient(url, on_channel_message=on_channel_message)
    client.connect()


    try:
        name = input('name: ')
        # Subscribe to the chat channel
        client.call_router('subscribe', 'chat-route', callback=on_subscribed, channel='test')

        message = input()
        while message != 'q!':
            # Send message
            client.call_router('chat', 'chat-route', name=name, message=message)
            message = input()
    except KeyboardInterrupt:
        client.disconnect()
