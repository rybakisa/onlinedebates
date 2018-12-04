from channels import route

channel_routing = [
    # Called when WebSockets connect
    route("websocket.connect", 'tournament.consumers.ws_connect', path=r'^/chat/(?P<room>\w+)$'),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", 'tournament.consumers.ws_echo'),
]