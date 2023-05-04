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
    inputSceretKey = request.GET.get('SecretKey', None)
    if (DeviceID is None) | len(DeviceID) < 8 :
        return HttpResponseBadRequest("参数错误")
    a = str(time.time())
    res = DeviceID + a
    res = base64.b64encode(res.encode('utf-8'))
    if inputSceretKey != "0":
        try:
            finduser = User.objects.get(SecretKey = inputSceretKey)
        except finduser.DoesNotExist:
            return JsonResponse({'StatusCode': 401})
        finduser.NewSessionToken = res
        User.save()
    return HttpResponse(base64.b64encode(res))

def CheckSessionToken(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
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
        firsttime = str(injson['SessionToken'])
        DeviceID = injson['DeviceID']
        firsttime = base64.b64decode(base64.b64decode(firsttime))
        firsttime = str(firsttime)
        firsttime = firsttime[2:len(firsttime)-1]
    except:
        return JsonResponse({'StatusCode': 418})
    if str(firsttime[0:len(DeviceID)]) == DeviceID:# 判断是否同一DeviceID
        firsttime = firsttime[len(DeviceID):len(firsttime)]
        stilltime = time.time() - float(firsttime)
        if stilltime < 600:
            return JsonResponse({'StatusCode': 200})
        else:
            return JsonResponse({'StatusCode': 401})
    else:
        return JsonResponse({'StatusCode': 401})

def Login(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
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
        firsttime = str(injson['SessionToken'])
        inputUserName = injson['UserName']
        DeviceID = injson['DeviceID']
        inputpwd = injson['Password']
        capthaCode = injson['CAPTCHACode']
        firsttime = base64.b64decode(base64.b64decode(firsttime))
        firsttime = str(firsttime)
        firsttime = firsttime[2:len(firsttime)-1]
        if capthaCode != "1":
            return JsonResponse({'StatusCode': 401})
        if str(firsttime[0:len(DeviceID)]) == DeviceID:  # 判断是否同一DeviceID
            firsttime = firsttime[len(DeviceID):len(firsttime)]
            stilltime = time.time() - float(firsttime)
            if stilltime >= 600:
                return JsonResponse({'StatusCode': 401})
        else:
            return JsonResponse({'StatusCode': 401})
    except:
        return JsonResponse({'StatusCode': 418})
    finduser = User.objects.values()
    finduser = list(finduser.filter(UserName = inputUserName))
    if finduser is None:
        return JsonResponse({'StatusCode': 401})
    if finduser[0]['Password'] == inputpwd:
        return JsonResponse({'StatusCode': 200, 'SecretKey': finduser[0]['SecretKey'], 'UID': finduser[0]['UID']})
    return JsonResponse({'StatusCode': 401})