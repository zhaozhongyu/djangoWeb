# -*- coding:utf-8 -*-
from django.db import models
import uuid, datetime
# Create your models here.
class Host(models.Model):
    host_ip = models.GenericIPAddressField(primary_key=True)
    host_user = models.CharField(max_length=15, default='root')
    host_password = models.CharField(max_length=64, default='Huawei123')

class Modules(models.Model):
    module_name = models.CharField(max_length=128, primary_key=True)
    module_onceonly = models.BooleanField(default=True) #这里表示是不是持续作用的, 比如说rcntp stop 就是一次性的
    # 如果是一次性的module, 则在到stop time时主动去登录环境进行stop操作, 否则由脚本控制自动停止
    module_description = models.CharField(max_length=2048)


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    hosts = models.ManyToManyField(Host)
    modules = models.ManyToManyField(Modules)
