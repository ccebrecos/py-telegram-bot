from setuptools import setup

setup(
    name='py-telegram-bot',
    version='0.1',
    description='Telegram bot coded in Python to retrieve Bitcoin data',
    license='Apache License v2.0',
    author='Carlos GC',
    author_email='mail@ccebrecos.com',
    url='https://github.com/ccebrecos/py-telegram-bot',
    keywords=[
        'bitcoin',
        'bitcoin api',
        'Telegram',
        'Bot'
    ],
    install_requires=[
        'json-rpc',
        'pyTelegramBotAPI',
        'websocket-client'
    ]
)
