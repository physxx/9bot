'''Sample Slack ping bot using asyncio and websockets.'''
import asyncio
import json
import signal
import aiohttp

from getPosts import checkCommand
from config import DEBUG, TOKEN

import websockets


RUNNING = True

async def api_call(method, data=None, file=None, token=TOKEN):
    '''
    Perform an API call to Slack.
    :param method: Slack API method name.
    :param type: str
    :param data: Form data to be sent.
    :param type: dict
    :param file: file pointer to send (for files.upload).
    :param type: file
    :param token: OAuth2 tokn
    :param type: str
    '''
    with aiohttp.ClientSession() as session:
        form = aiohttp.FormData(data or {})
        form.add_field("token", token)
        if file:
            form.add_field("file", file)
        async with session.post('https://slack.com/api/{0}'.format(method),
                                data=form) as response:
            assert 200 == response.status, ("{0} with {1} failed."
                                            .format(method, data))
            return await response.json()


async def producer(send, timeout=20):
    '''Produce a ping message every timeout seconds.'''
    while RUNNING:
        await asyncio.sleep(timeout)
        send({"type": "ping"})


async def consumer(message):
    '''Consume the message by printing it.'''
    message = json.loads(message)
    if message.get('type') == 'message':
        user_info = await api_call('users.info', dict(user=message.get('user')))
        #print("{user[user][name]}: {message[text]}".format(user=user_info, message=message))
        if message['channel'].startswith('D'):
            userChannel = message['channel']
            if 'user' in user_info:
                msg = checkCommand(message['text'].lower())
                txt = "9GAG"
                for post in msg:
                    if not post.startswith('['):
                        txt = post
                    await api_call("chat.postMessage", {"channel":userChannel, "text":txt,"attachments":post})


async def bot(get, token=TOKEN):
    '''Create a bot that joins Slack.'''
    rtm = await api_call("rtm.start")
    assert 'ok' in rtm and rtm['ok'], "Error connecting to RTM."

    async with websockets.connect(rtm["url"]) as ws:
        while RUNNING:
            listener_task = asyncio.ensure_future(ws.recv())
            producer_task = asyncio.ensure_future(get())

            done, pending = await asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            if listener_task in done:
                message = listener_task.result()
                asyncio.ensure_future(consumer(message))

            if producer_task in done:
                message = producer_task.result()
                await ws.send(message)


def stop():
    '''Gracefully stop the bot.'''
    global RUNNING
    RUNNING = False
    print("Stopping... closing connections.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    outbox = asyncio.Queue()


    loop.run_until_complete(asyncio.wait((bot(outbox.get),
                                          producer(outbox.put))))
    loop.close()
