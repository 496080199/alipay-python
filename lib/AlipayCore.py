#!/usr/bin/env python
#coding=utf-8
'''
#=============================================================================
#     FileName: AlipayCore.py
#         Desc: 支付宝接口共用函数类
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2011-09-24 03:32:13
#=============================================================================
'''

import hashlib
import os.path

class Core:
    def __init__(self):
        pass

    # 生成签名结果
    # <param name="sArray">要签名的数组</param>
    # <param name="key">安全校验码</param>
    # <param name="sign_type">签名类型</param>
    # <param name="input_charset">编码格式</param>
    # <returns>签名结果字符串</returns>
    @staticmethod
    def BuildMysign(paramDic,key,sign_type,input_charset):
        prestr = Core.CreateLinkString(paramDic)  #把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
        prestr = prestr + key                      #把拼接后的字符串再与安全校验码直接连接起来
        mysign = Core.Sign(prestr, sign_type, input_charset)	#把最终的字符串签名，获得签名结果
        return mysign

    # <summary>
    # 除去数组中的空值和签名参数
    # </summary>
    # <param name="dicArrayPre">过滤前的参数组</param>
    # <returns>过滤后的参数组</returns>
    @staticmethod
    def FilterPara(paramDicPre):
        paramDic ={}
        for key in paramDicPre:
            if key.lower() != "sign" and key.lower() != "sign_type" and paramDicPre[key] != "" and paramDicPre[key]!= None:
                paramDic[key]=paramDicPre[key]
        return paramDic

    # <summary>
    # 把数组所有元素排序，按照“参数=参数值”的模式用“&”字符拼接成字符串
    # </summary>
    # <param name="sArray">需要拼接的数组</param>
    # <returns>拼接完成以后的字符串</returns>
    @staticmethod
    def CreateLinkString(paramDic):
        paramKeys=paramDic.keys()
        #排序
        paramKeys.sort()
        preList=[]
        for key in paramKeys:
            preList.append('%s=%s'% (key,paramDic[key]))
        joined_string='&'.join(preList)
        return joined_string

    # <summary>
    # 签名字符串
    # </summary>
    # <param name="prestr">需要签名的字符串</param>
    # <param name="sign_type">签名类型,这里支持只MD5</param>
    # <param name="input_charset">编码格式</param>
    # <returns>签名结果</returns>
    @staticmethod
    def Sign(prestr,sign_type,input_charset):
        prestr=prestr.encode(input_charset)
        if (sign_type.upper() == "MD5"):
            hash=hashlib.md5()
            hash.update(prestr)
            result=hash.hexdigest()
        else:
            result=sign_type+u'方式签名尚未开发，清自行添加'
        return result

    # <summary>
    # 写日志，方便测试（网站需求，可以改成把记录存入数据库）
    # </summary>
    # <param name="sWord">要写入日志里的文本内容</param>
    @staticmethod
    def LogResult(sWord):
        strPath = os.path.dirname(__file__)
        strPath = os.path.join(strPath, "log.txt")
        f=file(strPath,'a') 
        f.write(time.strftime("%y-%m-%d-%H:%M:%S  ")+sWord)
        f.close()
