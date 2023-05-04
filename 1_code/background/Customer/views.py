import base64
import json
import time

from django.shortcuts import render
from django.http import *
from databaseManagementLocal.models import User

# Create your views here.
def testsessionid(firsttime):
    try: # 处理数据，如果数据被修改不符合加密要求，那就返回418
        firsttime = base64.b64decode(base64.b64decode(firsttime))
        firsttime = str(firsttime)
        firsttime = firsttime[2:len(firsttime)-1]
        firsttime = firsttime[8:len(firsttime)]
        stilltime = time.time() - float(firsttime)
        if stilltime <= 600:
            return True
        else:
            return False
    except:
        return False

def PersonalInformationView(request):
    if request.method == 'POST':
        try:
            request.params = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    # 非POST请求
    else:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try: # 处理数据，如果数据被修改不符合加密要求，那就返回418
        injson = request.params
        SessionToken = str(injson['SessionToken'])
        UID = injson['UID']
        SecretKey = injson['SecretKey']
    except:
        return JsonResponse({'StatusCode': 418})

    return JsonResponse({'ret': 500, 'msg': testsessionid(SessionToken)})
def ModifyPersonalInformation(request):
    return JsonResponse({'ret': 500, 'msg': '不支持该类型http请求'})
def ViewShoppingCart(request):
    return JsonResponse({'ret': 500, 'msg': '不支持该类型http请求'})
def ModifyShoppingCart(request):
    return JsonResponse({'ret': 500, 'msg': '不支持该类型http请求'})
def MakeOrder(request):
    return JsonResponse({'ret': 500, 'msg': '不支持该类型http请求'})
def OrderList(request):
    return JsonResponse({'ret': 500, 'msg': '不支持该类型http请求'})
def CheckOrder(request):
    return JsonResponse({'ret': 500, 'msg': '不支持该类型http请求'})