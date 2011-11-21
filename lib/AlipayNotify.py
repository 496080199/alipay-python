#!/usr/bin/env python
#coding=utf-8
'''
#=============================================================================
#     FileName: AlipayNotify.py
#         Desc: 支付宝通知处理类
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2011-09-27 00:52:09
#=============================================================================
'''
 
from AlipayConfig import Config
from AlipayCore import Core
import urllib2

# #///////////////////注意/////////////////////////////
# 调试通知返回时，可查看或改写log日志的写入TXT里的数据，来检查通知返回是否正常 
# </summary>
class Notify :
    #HTTPS支付宝通知路径
    Https_veryfy_url = "https://www.alipay.com/cooperate/gateway.do?service=notify_verify&"
    #HTTP支付宝通知路径
    Http_veryfy_url = "http://notify.alipay.com/trade/notify_query.do?"

    # 从配置文件中初始化变量
    # <param name="inputPara">通知返回参数数组</param>
    # <param name="notify_id">通知验证ID</param>
    def __init__(self):
        config=Config()
        #合作身份者ID
        self.partner = config.partner
        #交易安全校验码
        self.key = config.key
        self.input_charset = config.input_charset
        #签名方式
        self.sign_type = config.sign_type
        #访问模式
        self.transport = config.transport

    # <summary>
    #  验证消息是否是支付宝发出的合法消息
    # </summary>
    # <param name="inputPara">通知返回参数数组</param>
    # <param name="notify_id">通知验证ID</param>
    # <param name="sign">支付宝生成的签名结果</param>
    # <returns>验证结果</returns>
    def Verify(self,inputPara,notify_id, sign):
        #获取返回回来的待签名数组签名后结果
        mysign = self.GetResponseMysign(inputPara)
        #获取是否是支付宝服务器发来的请求的验证结果
        responseTxt = "true"
        if notify_id != "" :
            responseTxt = self.GetResponseTxt(notify_id)

        #写日志记录（若要调试，请取消下面两行注释）
        #sWord = "responseTxt=" + responseTxt + "\n sign=" + sign + "&mysign=" + mysign + "\n 返回回来的参数：" + GetPreSignStr(inputPara) + "\n "
        #Core.LogResult(sWord)

        #验证
        #responsetTxt的结果不是true，与服务器设置问题、合作身份者ID、notify_id一分钟失效有关
        #mysign与sign不等，与安全校验码、请求时的参数格式（如：带自定义参数等）、编码格式有关
        if responseTxt == "true" and sign == mysign:#验证成功
            return True
        else:#验证失败
            return False

    # <summary>
    # 获取待签名字符串（调试用）
    # </summary>
    # <param name="inputPara">通知返回参数数组</param>
    # <returns>待签名字符串</returns>
    def GetPreSignStr(self,inputPara):
        sPara = {}
        #过滤空值、sign与sign_type参数
        sPara = Core.FilterPara(inputPara)
        #获取待签名字符串
        preSignStr = Core.CreateLinkString(sPara)
        return preSignStr

    # <summary>
    # 获取返回回来的待签名数组签名后结果
    # </summary>
    # <param name="inputPara">通知返回参数数组</param>
    # <returns>签名结果字符串</returns>
    def GetResponseMysign(self,inputPara):
        sPara ={}
        #过滤空值、sign与sign_type参数
        sPara = Core.FilterPara(inputPara)
        #获得签名结果
        mysign = Core.BuildMysign(sPara, self.key, self.sign_type, self.input_charset)
        return mysign

    # <summary>
    # 获取是否是支付宝服务器发来的请求的验证结果
    # </summary>
    # <param name="notify_id">通知验证ID</param>
    # <returns>验证结果</returns>
    def GetResponseTxt(self,notify_id,timeout=120000):
        veryfy_url = self.transport == "https" and self.Https_veryfy_url or self.Http_veryfy_url
        veryfy_url += "partner=" + self.partner + "&notify_id=" + notify_id

        #获取远程服务器ATN结果，验证是否是支付宝服务器发来的请求
        open = urllib2.urlopen(veryfy_url, timeout=timeout)
        return open.read()
