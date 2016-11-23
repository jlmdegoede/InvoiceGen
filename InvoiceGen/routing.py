from channels.routing import route
from Invoices import consumers

channel_routing = [
    route("websocket.connect", consumers.ws_connect),
    route("websocket.receive", consumers.ws_receive),
]
