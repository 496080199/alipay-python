#!/usr/bin/env python
#coding=utf-8
'''
#=============================================================================
#     FileName: AlipaySubmit.py
#         Desc: 支付宝各接口请求提交类
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2011-09-24 14:20:35
#=============================================================================
'''
from AlipayConfig import Config
from AlipayCore import Core

class Submit:
    def __init__(self):
        config=Config()
        #交易安全校验码
        self.key = config.key
        #编码格式
        self.input_charset = config.input_charset
        #签名方式
        self.sign_type = config.sign_type

    # 生成要请求给支付宝的参数数组
    # <param name="sParaTemp">请求前的参数List</param>
    # <returns>要请求的参数List</returns>
    def BuildRequestPara(self,sParaTemp):
        #待签名请求参数数组
        sPara={}
        #签名结果
        mysign = ""

        #过滤签名参数数组
        sPara = Core.FilterPara(sParaTemp)

        #获得签名结果
        ##########################################################################################
        mysign = Core.BuildMysign(sPara, self.key, self.sign_type, self.input_charset)

        #签名结果与签名方式加入请求提交参数组中
        sPara["sign"]=mysign
        sPara["sign_type"]= self.sign_type
        return sPara

    # 生成要请求给支付宝的参数数组
    # <param name="sParaTemp">请求前的参数数组</param>
    # <returns>要请求的参数数组字符串</returns>
    def BuildRequestParaToString(self,sParaTemp):
        #待签名请求参数数组
        sPara ={}
        sPara = BuildRequestPara(sParaTemp)

        #把参数组中所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
        strRequestData = Core.CreateLinkString(sPara)
        return strRequestData

    # <summary>
    # 构造提交表单HTML数据
    # </summary>
    # <param name="sParaTemp">请求参数数组</param>
    # <param name="gateway">网关地址</param>
    # <param name="strMethod">提交方式。两个值可选：post、get</param>
    # <param name="strButtonValue">确认按钮显示文字</param>
    # <returns>提交表单HTML文本</returns>
    def BuildFormHtml(self,sParaTemp,gateway,strMethod,strButtonValue):
        #待请求参数数组
        dicPara ={}
        dicPara = self.BuildRequestPara(sParaTemp)

        sbHtml =[]

        sbHtml.append("<form id='alipaysubmit' name='alipaysubmit' action='" + gateway +
                "_input_charset=" + self.input_charset + "' method='" + strMethod.lower() + "'>")

        for key in dicPara:
            sbHtml.append("<input type='hidden' name='%s' value='%s' />" %(key,dicPara[key]))

        #submit按钮控件请不要含有name属性
        sbHtml.append("<input type='submit' value='" + strButtonValue + "' style='display:none'></form>")

        sbHtml.append("<script>document.forms['alipaysubmit'].submit()</script>")

        return ''.join(sbHtml)

####################未完成#######################################
'''
    # <summary>
    # 构造模拟远程HTTP的POST请求，获取支付宝的返回XML处理结果
    # </summary>
    # <param name="sParaTemp">请求参数数组</param>
    # <param name="gateway">网关地址</param>
    # <returns>支付宝返回XML处理结果</returns>
    def SendPostInfo(sParaTemp,gateway):
        #待请求参数数组字符串
        strRequestData = BuildRequestParaToString(sParaTemp)

        #把数组转换成流中所需字节数组类型

        Encoding code = Encoding.GetEncoding(self.input_charset)
        byte[] bytesRequestData = code.GetBytes(strRequestData)

        #构造请求地址
        strUrl = gateway + "_input_charset=" + self.input_charset

        #请求远程HTTP
        XmlDocument xmlDoc = new XmlDocument()
        try:
            #设置HttpWebRequest基本信息
            HttpWebRequest myReq = (HttpWebRequest)HttpWebRequest.Create(strUrl)
            myReq.Method = "post"
            myReq.ContentType = "application/x-www-form-urlencoded"

            #填充POST数据
            myReq.ContentLength = bytesRequestData.Length
            Stream requestStream = myReq.GetRequestStream()
            requestStream.Write(bytesRequestData, 0, bytesRequestData.Length)
            requestStream.Close()

            #发送POST数据请求服务器
            HttpWebResponse HttpWResp = (HttpWebResponse)myReq.GetResponse()
            Stream myStream = HttpWResp.GetResponseStream()

            #获取服务器返回信息
            XmlTextReader Reader = new XmlTextReader(myStream)
            xmlDoc.Load(Reader)
        except Exception as exp:
            strXmlError = "<error>" + exp + "</error>"
            xmlDoc.LoadXml(strXmlError)

        return xmlDoc
    }

    # <summary>
    # 构造模拟远程HTTP的GET请求，获取支付宝的返回XML处理结果
    # </summary>
    # <param name="sParaTemp">请求参数数组</param>
    # <param name="gateway">网关地址</param>
    # <returns>支付宝返回XML处理结果</returns>
    public static XmlDocument SendGetInfo(SortedDictionary<string, string> sParaTemp, string gateway)
    {
        #待请求参数数组字符串
        string strRequestData = BuildRequestParaToString(sParaTemp)

        #构造请求地址
        string strUrl = gateway + strRequestData

        #请求远程HTTP
        XmlDocument xmlDoc = new XmlDocument()
        try
        {
            #设置HttpWebRequest基本信息
            HttpWebRequest myReq = (HttpWebRequest)HttpWebRequest.Create(strUrl)
            myReq.Method = "get"

            #发送POST数据请求服务器
            HttpWebResponse HttpWResp = (HttpWebResponse)myReq.GetResponse()
            Stream myStream = HttpWResp.GetResponseStream()

            #获取服务器返回信息
            XmlTextReader Reader = new XmlTextReader(myStream)
            xmlDoc.Load(Reader)
        }
        catch (Exception exp)
        {
            string strXmlError = "<error>" + exp.Message + "</error>"
            xmlDoc.LoadXml(strXmlError)
        }

        return xmlDoc
    }
}
'''
