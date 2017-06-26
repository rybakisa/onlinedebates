import json
from urllib import parse
import logging

from channels import Group
from channels.sessions import channel_session


@channel_session
def ws_connect(message, room):
    query = parse.parse_qs(message['query_string'])
    if b'username' not in query:
        return
    logging.info('Adding websocket with username %s in room %s',
                 query[b'username'][0].decode('utf-8'), room)
    Group('chat-%s' % room).add(message.reply_channel)
    message.channel_session['room'] = room
    message.channel_session['username'] = query[b'username'][0].decode('utf-8')
    message.reply_channel.send({'accept': True})


@channel_session
def ws_echo(message):
    if 'username' not in message.channel_session:
        return
    room = message.channel_session['room']
    logging.info('Echoing message %s from username %s in room %s',
                 message.content['text'], message.channel_session['username'],
                 room)
    Group('chat-%s' % room).send({
        'text': json.dumps({
            'message': message.content['text'],
            'username': message.channel_session['username']
        }),
    })