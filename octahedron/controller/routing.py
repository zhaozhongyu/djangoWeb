#-------------------------------------------------------------------------------
#!/usr/bin/env python3 
# Project:     octahedron
# Name:        routing
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------

from channels.routing import route, include
from .Consumer import ws_connect, ws_message, ws_disconnect
channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    #Consumer.Consumer.as_route(path=r"^/chat/"),
]
'''
http_routing = [
    route("http.request",ws_message, path=r"^/poll/$", method=r"^POST$"),
]
chat_routing = [
    route("websocket.connect",ws_connect, path=r"^/(?P<room>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect),
]
'''
routing = [
    # You can use a string import path asthe first argument as well.
    include(channel_routing, path=r"^/websocket_log/$"),
    #include(http_routing),
]
