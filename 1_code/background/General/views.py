import base64
import json
import time

from django.http import *
from django.shortcuts import render
from databaseManagementLocal.models import User


# Create your views here.

def GetSessionToken(request):
    # 检查url中是否有参数deviceid
    DeviceID = request.GET.get('DeviceID', None)
    if (DeviceID is None) | len(DeviceID) < 8 :
        return HttpResponseBadRequest("参数错误")
    a = str(time.time())
    res = DeviceID + a
    res = base64.b64encode(res.encode('utf-8'))
    return HttpResponse(base64.b64encode(res))

def CheckSessionToken(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'POST':
        request.params = json.loads(request.body)
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    else:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        return HttpResponseBadRequest("请求方式错误")


        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})