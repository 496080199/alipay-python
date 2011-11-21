#encoding=utf-8

from django.conf.urls.defaults import patterns,include,url
from views import *

urlpatterns=patterns('alipay.views',
        url(r'checkout$',alipayTo),
        url(r'alipay_notify$',alipay_notify),
        url(r'alipay_return$',alipay_return),
    )
