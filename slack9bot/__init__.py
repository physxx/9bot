"""
    Module allowing to start a bot connecting to Slack through Slakp API. 
    User can then ask the bot if a Twitch streamer is streaming. 
"""
import os
import asyncio

from .slack9bot import consumer, stop, api_call, producer

def main():
    loop = asyncio.get_event_loop()
    outbox = asyncio.Queue()
    loop.run_until_complete(asyncio.wait((bot(outbox.get),producer(outbox.put))))
    loop.close()