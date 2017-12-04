#-------------------------------------------------------------------------------
#!/usr/bin/env python3 
# Project:     octahedron
# Name:        Consumer
# Purpose:     
# Author:      zWX206936
# Created:     2017/11/21 19:06
# Copyright:   (c) "zWX206936" "2017/11/21 19:06" 
# Licence:     <your licence>
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
from channels import Group
from channels.sessions import channel_session
from .models import *
from .operation.BatchExecute import BatchExecute
from .operation.preExecute import preExecute
import time
from channels.message import Message
from controller.operation.websocket import websocket

@channel_session
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    client = message.get("client")[0] #获取ip
    message.channel_session["client"] = client
    print(message.channel_session["client"])
    group = Group(client)
    group.add(message.reply_channel)
    message.reply_channel.send({"accept": True})

    # Save room in session and add us to the group


# 设计中网页端只会往服务器发一条信息, 就是task.id, 然后服务器根据task.id 启动对应任务, 并且将channel传给对应的线程
# Connected towebsocket.receive
#@enforce_ordering
@channel_session
def ws_message(message):
    id = message.get("text")
    if id == "ping":
        return ;
    client = message.channel_session["client"]
    group = Group(client)
    threads = []
    print("accept task id:" + id)
    task = Task.objects.get(id= id)
    group.send({"text": "[INFO][ALL][ALL]"+ getTime() +"begin to execute modules."}, immediately=True)

    for host in task.hosts.all():
        pre = preExecute(host, group)
        pre.run() #当前不做多线程上传, 后续可以修改优化

    for host in task.hosts.all():
        for _module in task.modules.all():
            batch = BatchExecute(host, _module, group)
            batch.start()
            threads.append(batch)
    while len(threads) > 0:
        for batch in threads:
            time.sleep(3)
            if not batch.is_alive():
                threads.remove(batch)
    group.send({"text": "[INFO][ALL][ALL]"+ getTime() +"end to execute modules."}, immediately=True)
    time.sleep(5)
    group.send({"close": True})

    #message.reply_channel.send({"text":"receive message"})

# Connected towebsocket.disconnect
@channel_session
def ws_disconnect(message):
    print("socket close")
    message.reply_channel.send({"close":True})
    client = message.channel_session["client"]
    group = Group(client)
    group.discard(message.reply_channel)

def getTime():
    now = datetime.datetime.now()
    return "[" + now.strftime('%H:%M:%S') + "]"

