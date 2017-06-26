from channels import route
from .consumers import *


# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We could path match here if we wanted.
websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ws_connect, path=r'^/chat/(?P<room>\w+)$'),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_echo),
]