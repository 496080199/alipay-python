#!/usr/bin/env python
#coding=utf-8
'''
#=============================================================================
#     FileName: AlipayService.py
#         Desc: 支付宝接口构造类
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2011-09-24 01:47:10
#=============================================================================
'''
from AlipayConfig import Config
from AlipaySubmit import Submit

# 要传递的参数要么不允许为空，要么就不要出现在数组与隐藏控件或URL链接里。
class Service:
    # 构造函数
    def __init__(self):
        # 从配置文件及入口文件中初始化变量
        config=Config()
        #合作者身份ID
        self.partner = config.partner
        #字符编码格式
        self.input_charset = config.input_charset
        #签约支付宝账号或卖家支付宝帐户
        self.seller_email = config.seller_email
        #页面跳转同步返回页面文件路径
        self.return_url = config.return_url
        #服务器通知的页面文件路径
        self.notify_url =config.notify_url 
        #支付宝网关地址（新）
        self.GATEWAY_NEW = "https://mapi.alipay.com/gateway.do?"

    # 构造即时到帐接口
    # <param name="sParaTemp">请求参数集合</param>
    # <returns>表单提交HTML信息</returns>
    def Create_direct_pay_by_user(self,sParaTemp):
        #增加基本配置
        sParaTemp["service"]="create_direct_pay_by_user"
        sParaTemp["partner"]=self.partner
        sParaTemp["_input_charset"]= self.input_charset
        sParaTemp["seller_email"]= self.seller_email
        sParaTemp["return_url"]=self.return_url
        sParaTemp["notify_url"]= self.notify_url

        #确认按钮显示文字
        strButtonValue = u"确认"
        #表单提交HTML数据
        strHtml = ""

        #构造表单提交HTML数据
        submit=Submit()
        strHtml = submit.BuildFormHtml(sParaTemp, self.GATEWAY_NEW, "get", strButtonValue)

        return strHtml

    #未完成
    # 用于防钓鱼，调用接口query_timestamp来获取时间戳的处理函数
    # <returns>时间戳字符串</returns>
    def Query_timestamp(self):
        url = self.GATEWAY_NEW + "service=query_timestamp&partner=" + Config.partner
        encrypt_key = ""

        #从网络读取xml，未完成
        #XmlTextReader Reader = new XmlTextReader(url)
        #XmlDocument xmlDoc = new XmlDocument()
        #xmlDoc.Load(Reader)
        #encrypt_key = xmlDoc.SelectSingleNode("/alipay/response/timestamp/encrypt_key").InnerText

        return encrypt_key


    #******************若要增加其他支付宝接口，可以按照下面的格式定义******************//
    # <summary>
    # 构造(支付宝接口名称)接口
    # </summary>
    # <param name="sParaTemp">请求参数集合List</param>
    # <returns>表单提交HTML文本或者支付宝返回XML处理结果</returns>
    def AlipayInterface(self,sParaTemp):
        #增加基本配置

        #表单提交HTML数据变量
        strHtml = ""

        #构造请求参数数组

        #构造给支付宝处理的请求
        #请求方式有以下三种：
        #1.构造表单提交HTML数据:Submit.BuildFormHtml()
        #2.构造模拟远程HTTP的POST请求，获取支付宝的返回XML处理结果:Submit.SendPostInfo()
        #3.构造模拟远程HTTP的GET请求，获取支付宝的返回XML处理结果:Submit.SendGetInfo()
        #请根据不同的接口特性三选一

        return strHtml
