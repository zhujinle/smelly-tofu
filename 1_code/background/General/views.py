import base64
import json
import time

from django.contrib.auth import authenticate, login
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

def GetMenuList(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        # SessionToken = request.POST.get('SessionToken', None)
        SecretKey = request.POST.get('SecretKey')
        if SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})

    try:
        finduser = User.objects.get(SecretKey=SecretKey)
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    if finduser.Type == 1:
        return JsonResponse({"StatusCode":200,"List":[{"id":100,"authName":"用户功能","path":None,"children":[{"id":101,"authName":"点菜","path":"makeorder","children":[]},{"id":102,"authName":"购物车管理","path":"cartview","children":[]}]},{"id":300,"authName":"订单管理","path":None,"children":[{"id":301,"authName":"订单列表","path":"orderlist","children":[]}]},{"id":500,"authName":"个人信息","path":None,"children":[{"id":501,"authName":"个人信息查看","path":"myinfo","children":[]},{"id":502,"authName":"个人信息修改","path":"myinfoedit","children":[]},{"id":503,"authName":"个人数据看板","path":"mydashboard","children":[]}]}]})
    elif finduser.Type == 2:
        return JsonResponse({"StatusCode":200,"List":[{"id":200,"authName":"菜单管理","path":None,"children":[{"id":201,"authName":"食品列表","path":"menuview","children":[]}]},{"id":300,"authName":"订单管理","path":None,"children":[{"id":301,"authName":"订单列表","path":"orderlist","children":[]},{"id":304,"authName":"可用配送员查看","path":"deliverystaffview","children":[]},{"id":305,"authName":"通知配送","path":"deliverypush","children":[]}]},{"id":500,"authName":"个人信息","path":None,"children":[{"id":501,"authName":"个人信息查看","path":"myinfo","children":[]},{"id":502,"authName":"个人信息修改","path":"myinfoedit","children":[]},{"id":503,"authName":"个人数据看板","path":"mydashboard","children":[]}]}]})
    elif finduser.Type == 3:
        return JsonResponse({"StatusCode":200,"List":[{"id":300,"authName":"订单管理","path":None,"children":[{"id":301,"authName":"订单列表","path":"orderlist","children":[]}]},{"id":500,"authName":"个人信息","path":None,"children":[{"id":501,"authName":"个人信息查看","path":"myinfo","children":[]},{"id":502,"authName":"个人信息修改","path":"myinfoedit","children":[]},{"id":503,"authName":"个人数据看板","path":"mydashboard","children":[]}]}]})
    elif finduser.Type == 4:
        return JsonResponse({"StatusCode":200,"List":[{"id":100,"authName":"用户功能","path":None,"children":[{"id":101,"authName":"点菜","path":"makeorder","children":[]},{"id":102,"authName":"购物车管理","path":"cartview","children":[]}]},{"id":200,"authName":"菜单管理","path":None,"children":[{"id":201,"authName":"食品列表","path":"menuview","children":[]}]},{"id":300,"authName":"订单管理","path":None,"children":[{"id":301,"authName":"订单列表","path":"orderlist","children":[]},{"id":304,"authName":"可用配送员查看","path":"deliverystaffview","children":[]},{"id":305,"authName":"通知配送","path":"deliverypush","children":[]}]},{"id":400,"authName":"用户管理","path":None,"children":[{"id":401,"authName":"用户列表","path":"userlist","children":[]}]},{"id":500,"authName":"个人信息","path":None,"children":[{"id":501,"authName":"个人信息查看","path":"myinfo","children":[]},{"id":502,"authName":"个人信息修改","path":"myinfoedit","children":[]},{"id":503,"authName":"个人数据看板","path":"mydashboard","children":[]}]}]})
    return JsonResponse({'StatusCode': 418})

def Login(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        # SessionToken = request.POST.get('SessionToken', None)
        userName = request.POST.get('username')
        passWord = request.POST.get('password')
        if  userName is None or passWord is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    user = authenticate(username=userName, password=passWord)
    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                try:
                    finduser = User.objects.get(username= userName)
                except User.DoesNotExist:
                    return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
                # 在session中存入用户类型
                request.session['usertype'] = 'mgr'
                a = str(time.time())
                res = userName + a
                res = base64.b64encode(res.encode('utf-8'))
                finduser.SecretKey = str(base64.b64encode(res),'utf-8')
                finduser.save()
                return JsonResponse({'StatusCode': 200 , 'SecreyKey': finduser.SecretKey})
            else:
                request.session['usertype'] = 'usr'
                try:
                    finduser = User.objects.get(username= userName)
                except User.DoesNotExist:
                    return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
                # 在session中存入用户类型
                a = str(time.time())
                res = userName + a
                res = base64.b64encode(res.encode('utf-8'))
                finduser.SecretKey = str(base64.b64encode(res),'utf-8')
                finduser.save()
                return JsonResponse({'StatusCode': 200, 'SecreyKey': finduser.SecretKey})
        else:
            return JsonResponse({'StatusCode': 401, 'msg': '用户已经被禁用'})

        # 否则就是用户名、密码有误
    else:
        return JsonResponse({'StatusCode': 401, 'msg': '用户名或者密码错误'})
"""
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
"""