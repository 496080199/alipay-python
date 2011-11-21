#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

#记录订单的表，请根据自己需求完成
class Transaction(models.Model):
    out_trade_no=models.CharField(max_length=32)
    user=models.ForeignKey(User)
