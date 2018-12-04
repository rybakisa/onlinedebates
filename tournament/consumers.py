import json
import logging

from channels import Group
from channels.sessions import channel_session
from .models import ChatMessage, Player


@channel_session
def ws_connect(message, room):
    logging.info('Adding websocket in room %s', room)
    Group('chat-%s' % room).add(message.reply_channel)
    message.channel_session['room'] = room
    message.reply_channel.send({'accept': True})


@channel_session
def ws_echo(message):
    room = message.channel_session['room']
    logging.info('Echoing message %s in room %s', message.content['text'], room)
    content = message.content['text']
    content = json.loads(content)

    if content['event'] == 'chat':
        msg_from = Player.objects.get(pk=content['data']['from_id'])
        text = content['data']['text']

        # save to DB
        cm = ChatMessage(msg_from=msg_from, text=text)
        cm.save()

        # send message
        Group('chat-%s' % room).send({
            'text': json.dumps({
                'event': 'chat',
                'data': {
                    'from_name': msg_from.name,
                    'from_id': msg_from.pk,
                    'text': text,
                    'time': str(cm.time),
                },
            }),
        })
