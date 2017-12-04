#-------------------------------------------------------------------------------
#!/usr/bin/env python3 
# Project:     octahedron
# Name:        ssh_execute
# Purpose:     
# Licence:     <your licence>
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------

import paramiko

class ssh_execute():

    __ssh_fd = None
    def __init__(self, _host, _username, _password):
        try:
            _ssh_fd = paramiko.SSHClient()
            _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh_fd.connect(_host, username=_username, password=_password)
        except Exception as e:
            print('ssh %s@%s: %s' % (_username, _host, e))
            return ;
        self.__ssh_fd = _ssh_fd

    def __del__(self):
        if self.__ssh_fd:
            self.__ssh_fd.close()

    def execute(self, command):
        try:
            stdin, stdout, stderr = self.__ssh_fd.exec_command(command)
            sout = stdout.readlines()
            serr = stderr.readlines()
            if serr != []:
                raise Exception(serr)
            else:
                print(sout)
        except Exception as e:
            print("execute command %s error, error message is %s" % (command, serr))

    @property
    def client(self):
        return self.__ssh_fd
