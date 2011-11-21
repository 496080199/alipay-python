#!/usr/bin/env python
#coding=utf-8
'''
#=============================================================================
#     FileName: AlipayConfig.py
#         Desc: 基础配置类
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2011-11-21 13:53:39
#=============================================================================
'''

class Config:
    def __init__(self):
        #↓↓↓↓↓↓↓↓↓↓请在这里配置您的基本信息↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        #合作身份者ID，以2088开头由16位纯数字组成的字符串
        self.partner = ""
        #交易安全检验码，由数字和字母组成的32位字符串
        self.key = ""
        #签约支付宝账号或卖家支付宝帐户
        self.seller_email = ""
        #页面跳转同步返回页面文件路径 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
        self.return_url = ""
        #服务器通知的页面文件路径 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
        self.notify_url = ""
        #↑↑↑↑↑↑↑↑↑↑请在这里配置您的基本信息↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        #字符编码格式 目前支持 gbk 或 utf-8
        self.input_charset = "utf-8"
        #签名方式 不需修改
        self.sign_type = "MD5"
        #访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
        self.transport = "http"
