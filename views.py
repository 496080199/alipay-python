#!/usr/bin/env python
#coding=utf-8
'''
#=============================================================================
#     FileName: views.py
#         Desc: 支付宝接口调用类
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2011-11-21 13:52:52
#=============================================================================
'''
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response,RequestContext
from lib.AlipayService import Service
from lib.AlipayNotify import Notify
import hashlib
import time
from cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def alipayTo(request):
    #/////////////////////////////////////////请求参数////////////////////////////////////////
    #//////////必填参数//////////////////////////////////////////
    #请与贵网站订单系统中的唯一订单号匹配
    hash=hashlib.md5()
    hash.update(str(time.time())) 
    out_trade_no=hash.hexdigest()

    cart=Cart(request)
    #订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里
    subject = u""
    #订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    body = ""
    for item in cart:
        body="%s%sx%d+" % (body,item.product.name,item.quantity)
    body=body[:-1]
    #订单总金额，显示在支付宝收银台里的“应付总额”里
    total_fee = cart.total_fee 
    #////////// end of 必填参数/////////////////////////////////////

    #扩展功能参数——默认支付方式//
    #默认支付方式，代码见“即时到帐接口”技术文档
    paymethod = ""
    #默认网银代号，代号列表见“即时到帐接口”技术文档“附录”→“银行列表”
    defaultbank = ""

    #扩展功能参数——防钓鱼//
    #防钓鱼时间戳
    anti_phishing_key = ""
    #获取客户端的IP地址，建议：编写获取客户端IP地址的程序
    exter_invoke_ip = ""
    #注意：
    #请慎重选择是否开启防钓鱼功能
    #exter_invoke_ip、anti_phishing_key一旦被设置过，那么它们就会成为必填参数
    #建议使用POST方式请求数据
    #示例：
    #exter_invoke_ip = ""
    #Service aliQuery_timestamp = new Service()
    #anti_phishing_key = aliQuery_timestamp.Query_timestamp() 

    #扩展功能参数——其他//
    #商品展示地址，要用http:// 格式的完整路径，不允许加?id=123这类自定义参数
    show_url = ""
    #自定义参数，可存放任何内容（除=、&等特殊字符外），不会显示在页面上
    ##这里保存当前用户ID
    extra_common_param = str(request.user.id)
    #默认买家支付宝账号
    buyer_email = ""

    #扩展功能参数——分润(若要使用，请按照注释要求的格式赋值)//
    #提成类型，该值为固定值：10，不需要修改
    royalty_type = ""
    #提成信息集
    royalty_parameters = ""
    #注意：
    #与需要结合商户网站自身情况动态获取每笔交易的各分润收款账号、各分润金额、各分润说明。最多只能设置10条
    #各分润金额的总和须小于等于total_fee
    #提成信息集格式为：收款方Email_1^金额1^备注1|收款方Email_2^金额2^备注2
    #示例：
    #royalty_type = "10"
    #royalty_parameters = "111@126.com^0.01^分润备注一|222@126.com^0.01^分润备注二"
    #///////////////////////////////////end of 请求参数//////////////////////////////////////

    #把请求参数打包成数组
    sParaTemp = {}
    sParaTemp["payment_type"]= "1"
    sParaTemp["show_url"]= show_url
    sParaTemp["out_trade_no"]= out_trade_no
    sParaTemp["subject"]= subject
    sParaTemp["body"]= body
    sParaTemp["total_fee"]= total_fee
    sParaTemp["paymethod"]= paymethod
    sParaTemp["defaultbank"]= defaultbank
    sParaTemp["anti_phishing_key"]= anti_phishing_key
    sParaTemp["exter_invoke_ip"]= exter_invoke_ip
    sParaTemp["extra_common_param"]= extra_common_param
    sParaTemp["buyer_email"]= buyer_email
    sParaTemp["royalty_type"]= royalty_type
    sParaTemp["royalty_parameters"]= royalty_parameters

    #构造即时到帐接口表单提交HTML数据，无需修改
    alipay = Service()
    strHtml = alipay.Create_direct_pay_by_user(sParaTemp)
    return render_to_response("empty.html",{'content':strHtml})

def alipay_notify(request):
    if request.POST:
        notify = Notify()
        verifyResult = aliNotify.Verify(request.POST, 
                request.POST["notify_id"], request.POST["sign"])
        if verifyResult:#验证成功
            #///////////////////////////////////////////////////////////////////////////////////
            #请在这里加上商户的业务逻辑程序代码

            #——请根据您的业务逻辑来编写程序（以下代码仅作参考）——
            #获取支付宝的通知返回参数，可参考技术文档中服务器异步通知参数列表
            order_no = request.POST["out_trade_no"]     #获取订单号
            total_fee = request.POST["total_fee"]       #获取总金额
            subject = request.POST["subject"]           #商品名称、订单名称
            body = request.POST["body"]                 #商品描述、订单备注、描述

            if request.POST["trade_status"] == "TRADE_FINISHED"\
                    or request.POST["trade_status"] =="TRADE_SUCCESS":
                #判断该笔订单是否在商户网站中已经做过处理
                #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
                #如果有做过处理，不执行商户的业务程序
                return HttpResponse("success")  #请不要修改或删除
            else:
                return HttpResponse("success")  #其他状态判断。普通即时到帐中，其他状态不用判断，直接打印success。

            #——请根据您的业务逻辑来编写程序（以上代码仅作参考）——
            #/////////////////////////////////////////////////////////////////////////////////////
        else: #验证失败
            return HttpResponse("fail")
    else:
        return HttpResponse("无通知参数")

@login_required
def alipay_return(request):
    if request.GET:
        notify = Notify()
        verifyResult = aliNotify.Verify(request.GET, 
                request.GET["notify_id"], request.GET["sign"])
        if verifyResult:#验证成功
            #///////////////////////////////////////////////////////////////////////////////////
            #请在这里加上商户的业务逻辑程序代码

            #——请根据您的业务逻辑来编写程序（以下代码仅作参考）——
            #获取支付宝的通知返回参数，可参考技术文档中服务器异步通知参数列表
            order_no = request.GET["out_trade_no"]     #获取订单号
            total_fee = request.GET["total_fee"]       #获取总金额
            subject = request.GET["subject"]           #商品名称、订单名称
            body = request.GET["body"]                 #商品描述、订单备注、描述

            if request.GET["trade_status"] == "TRADE_FINISHED"\
                    or request.GET["trade_status"] =="TRADE_SUCCESS":
                #判断该笔订单是否在商户网站中已经做过处理
                #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
                #如果有做过处理，不执行商户的业务程序
                return HttpResponse("支付成功！") 
            else:
                return HttpResponse("支付成功!")  #其他状态判断。普通即时到帐中，其他状态不用判断，直接打印success。

            #——请根据您的业务逻辑来编写程序（以上代码仅作参考）——
            #/////////////////////////////////////////////////////////////////////////////////////
        else: #验证失败
            return HttpResponse("fail")
    else:
        return HttpResponse("无通知参数")
