#-------------------------------------------------------------------------------
#!/usr/bin/env python3 
# Project:     octahedron
# Name:        BatchExecute
# Purpose:     
# Author:      zWX206936
# Created:     2017/11/9 21:46
# Copyright:   (c) "zWX206936" "2017/11/9 21:46" 
# Licence:     <your licence>
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------

from threading import Thread

import datetime
import paramiko, os
#from controller.models import *

class BatchExecute(Thread):
    def __init__(self, __hostmodel, __module, group):
        super(BatchExecute, self).__init__()
        self.__channel = group
        self.__hostip = __hostmodel.host_ip
        self.__module = __module.module_name
        self.__username = __hostmodel.host_user
        self.__password = __hostmodel.host_password
        self.__sshclient = self.ssh_connect(self.__hostip, self.__username, self.__password)
        self.__currentpath = os.getcwd()
        self.__destdir = "/opt/uniagentdfr/"
        self.__sftpclient = None
    def __del__(self):
        self.__sshclient.close()

    def run(self):
        print("execute: "+"/bin/bash "+self.__destdir+self.__module+"/bin/start.sh")
        self.execute("nohup /bin/bash "+self.__destdir+self.__module+"/bin/start.sh "+ self.__hostip + " 2>&1 &")
        self.__del__();


    def ssh_connect(self,_host, _username, _password):
        try:
            _ssh_fd = paramiko.SSHClient()
            _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh_fd.connect(_host, username=_username, password=_password)
        except Exception as e:
            print('ssh %s@%s: %s' % (_username, _host, e))
            exit()
        return _ssh_fd

    def execute(self, command):
        try:
            self.__channel.send({"text":"[INFO][" + self.__hostip + "][" + self.__module + "]"+ self.getTime() +"begin to execute module."}, immediately=True)
            stdin, stdout, stderr = self.__sshclient.exec_command(command)
            for line in stdout:
                self.__channel.send({"text":line.strip("\n")}, immediately=True)
            self.__channel.send({"text": "[INFO]["+self.__hostip+"]["+self.__module +"]"+ self.getTime() +"end to execute module."}, immediately=True)
        except Exception as e:
            print("execute command %s error" % (command))

    def getTime(self):
        now = datetime.datetime.now()
        return "["+now.strftime('%H:%M:%S')+"]"

