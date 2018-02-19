# Py-telegram-bot

Python3 telegram bot made in order to listen bitcoin transactions and events on the Bitcoin network.


The bot has two main functionalities:
- RPC calls
- Push notifications to some events (currently new blocks & transactions events)


## Events
#### Blocks
In order to subscribe to new block events, the message to send to the bot is <code>/sub</code>. And to unsubscribe <code>/unsub</code>.

#### Transactions
For the address events, the messages are as follows:
<code>/listen \<addr> </code>
<code>/unlisten \<addr> </code>

## Configuration
All private configuration is under the following directory:
<code>res/private/</code>

To setup the bot, place your token at:

telegram.py:
```python
TOKEN = ""
```

To setup the rpc calls, fullfill the following data at:

rpc.py:
```python
URL = ""
AUTH = ('user', 'password')
```

And finally, to setup the push notifications, use an external websocket, place its data at:

ws.py:
```python
URL = ""
```


<> with ♥ by @ccebrecos
