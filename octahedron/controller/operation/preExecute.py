#-------------------------------------------------------------------------------
#!/usr/bin/env python3 
# Project:     octahedron
# Name:        preExecute
# Purpose:     
# Author:      zWX206936
# Created:     2017/11/10 14:21
# Copyright:   (c) "zWX206936" "2017/11/10 14:21" 
# Licence:     <your licence>
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
#将包上传并创建目录, 解压
import datetime
import paramiko, os,zipfile

class preExecute():
    def __init__(self, __hostmodel, group):
        self.__channel = group
        self.__hostip = __hostmodel.host_ip
        self.__username = __hostmodel.host_user
        self.__password = __hostmodel.host_password
        self.__sshclient = self.ssh_connect(self.__hostip, self.__username, self.__password)
        self.__currentpath = os.getcwd()
        self.__destdir = "/opt/uniagentdfr/"
        self.__sftpclient = None
    def __del__(self):
        self.__sshclient.close()
        try:
            self.__sftpclient.close()
        except:
            pass

    def run(self):
        self.execute('mkdir -p '+self.__destdir)
        filename = self.__currentpath+"/controller/static/controller/module.zip"
        #self.execute('sed -i "s/\#[[:space:]]*Subsystem[[:space:]]*sftp[[:space:]]*\/usr\/lib64\/ssh\/sftp-server/Subsystem  sftp \/usr\/lib64\/ssh\/sftp-server/g" /etc/ssh/sshd_config;')
       # self.execute("service sshd restart;")
        self.__channel.send({"text":"[INFO]["+self.__hostip+"][ALL]"+ self.getTime() +"begin to sftp send module package."}, immediately=True)
        self.sftp_put(filename, self.__destdir + "module.zip")
        self.__channel.send({"text":"[INFO]["+self.__hostip+"][ALL]"+ self.getTime() +"end to sftp send module package."}, immediately=True)
        self.execute("cd "+self.__destdir+ ";")
        self.execute("touch /opt/uniagentdfr/aaaaa;")
        self.execute("unzip -o /opt/uniagentdfr/module.zip  -d /opt/uniagentdfr/;")
        self.execute("chmod -R 755 *;")
        self.__channel.send({"text":"[INFO]["+self.__hostip+"][ALL]"+ self.getTime() +"chmod -R 755 * ."}, immediately=True)
        self.__del__();

    def ssh_connect(self,_host, _username, _password):
        try:
            _ssh_fd = paramiko.SSHClient()
            _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh_fd.connect(_host, username=_username, password=_password)
            return _ssh_fd
        except Exception as e:
            print('ssh %s@%s:passwd %s, error message is %s' % (_username, _host,_password, e))



    def sftp_open(self):
        if self.__sftpclient is None:
            self.__sftpclient = self.__sshclient.open_sftp()
        return ;

    def sftp_put(self, _put_from_path, _put_to_path):
        self.sftp_open()
        return self.__sftpclient.put(_put_from_path, _put_to_path)

    def sftp_get(self,_get_from_path, _get_to_path):
        self.__sftpclient = self.sftp_open(self.__sshclient)
        self.__sftpclient.get(_get_from_path, _get_to_path)
        self.__sftpclient.close()
        self.__sftpclient = None
        return ;

    def execute(self, command):
        try:
            stdin, stdout, stderr = self.__sshclient.exec_command(command)
            for line in stdout:
                self.__channel.send({"text":line.strip("\n")}, immediately=True)
        except Exception as e:
            print("execute command %s error, error message is %s" % (command, e))
            return ""

    def getTime(self):
        now = datetime.datetime.now()
        return "[" + now.strftime('%H:%M:%S') + "]"
