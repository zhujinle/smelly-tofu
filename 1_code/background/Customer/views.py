from django.shortcuts import render

# Create your views here.
import base64
import json
import os
import time

from django.shortcuts import render
from django.http import *
from databaseManagementLocal.models import User, Order, Menu
from django.db.models import Q, F


# Create your views here.

def PersonalInformationView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken',None)
        inputUID = request.POST.get('UID',None)
        SecretKey = request.POST.get('SecretKey',None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID = inputUID) & Q(Type=1))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    return JsonResponse({
        'StatusCode': 200,
        'UserName': FindUser.UserName,
        'AvatarUrl': '' if FindUser.Avatar.name == '' else FindUser.Avatar.url,
        'MenberStatus': FindUser.get_Member_display(),
        'MoneySum': FindUser.MoneySum,
        'Address': FindUser.Address,
        'Phone': FindUser.Phone
    })
def ModifyPersonalInformation(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken',None)
        inputUID = request.POST.get('UID',None)
        SecretKey = request.POST.get('SecretKey',None)
        inputUserName = request.POST.get('UserName',None)
        inputAvatar = request.FILES.get('AvatarUrl',None)
        inputAddress = request.POST.get('Address',None)
        imputphone = request.POST.get('Phone',None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(SecretKey=SecretKey) & Q(UID=inputUID) & Q(Type =1))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg':'无此用户'})
    if inputUserName is not None:
        finduser.UserName = inputUserName
    if inputAvatar is not None:
        finduser.Avatar = inputAvatar
    if inputAddress is not None:
        finduser.Address = inputAddress
    if imputphone is not None:
        finduser.Phone = imputphone
    finduser.save()
    return JsonResponse({'StatusCode': 200, 'UserName': inputUserName})
def ViewShoppingCart(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(SecretKey=SecretKey) & Q(UID=inputUID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    return JsonResponse({'StatusCode': 200, 'CartMenber': finduser.Cart})
def ModifyShoppingCart(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputCartMenber = request.POST.get('CartMenber',None)
        if SessionToken is None or inputUID is None or SecretKey is None or inputCartMenber is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(SecretKey=SecretKey) & Q(UID=inputUID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    finduser.Cart = inputCartMenber
    finduser.save()
    return JsonResponse({'StatusCode': 200})
def MakeOrder(request):
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        inputUID = request.POST.get('UID', None)
        SessionToken = request.POST.get('SessionToken', None)
        SecretKey = request.POST.get('SecretKey', None)
        Address = request.POST.get('Address', None)
        Phone = request.POST.get('Phone', None)
        Notes = request.POST.get('Notes', None)
        Payment = request.POST.get('Payment', None)
        OrderCheck = request.POST.get('OrderCheck',None)
        ShopID = request.POST.get('ShopUID', None)
        if inputUID is None or \
                SessionToken is None or \
                SecretKey is None or \
                Address is None or \
                Phone is None or \
                Notes is None or \
                Payment is None or \
                ShopID is None or \
                OrderCheck is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(SecretKey=SecretKey) & Q(UID=ShopID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    try:
        findShop = User.objects.get(Q(UID=inputUID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    Cart = finduser.Cart['CartNember']
    MoneySum = 0.0
    for each in Cart:
        try:
            findfood = Menu.objects.get(Q(ShopID__menu=ShopID) & Q(FoodID=each['Foodid']))
        except:
            return JsonResponse({'StatusCode': 418, 'msg': '无此食物'})
        MoneySum += findfood.Money*findfood.Discount
    res = Order.objects.create(UserUID=finduser,
                               Address=Address,
                               Phone=Phone,
                               Notes=Notes,
                               Payment=Payment,
                               ShopUID=ShopID,
                               Cart=finduser.Cart,
                               MoneySum=MoneySum)
    findShop.MoneyDaily += MoneySum
    findShop.MoneySum += MoneySum
    findShop.MoneyMonthly += MoneySum
    finduser.MoneyDaily += MoneySum
    finduser.MoneyMonthly += MoneySum
    finduser.MoneySum += MoneySum
    findShop.CustomerDaily += 1
    findShop.CustomerSum +=1
    return JsonResponse({'StatusCode': 200, 'OrderNumber': res.OrderNumber, 'PayUrl': 'http://127.0.0.1:8000/media/static/qrcode/'+str(int(MoneySum))+'.jpg'})

def ConfirmOrder(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken', None)
        SecretKey = request.POST.get('SecretKey', None)
        OrderMenber = request.POST.get('OrderNumber',None)
        if SessionToken is None or OrderMenber is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        findOrder = Order.objects.get(OrderNumber = OrderMenber)
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    findOrder.PayStatus = True
    findOrder.save()
    return JsonResponse({'StatusCode': 200})
def OrderList(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        if SessionToken is None or inputUID is None or SecretKey is None :
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        findOrder = Order.objects.filter(UserUID = inputUID).order_by(F('OrderNumber').desc())
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 200, 'OrderList': ''})
    findOrder = list(findOrder)
    for i in range(len(findOrder)):
        findOrder[i] = findOrder[i].OrderNumber
    return JsonResponse({'StatusCode': 200, 'OrderList': list(findOrder)})

def CheckOrder(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputOrderNumber = request.POST.get('OrderNumber', None)
        if SessionToken is None or inputUID is None or SecretKey is None or inputOrderNumber is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        findOrder = Order.objects.get(Q(UserUID=inputUID) & Q(OrderNumber=inputOrderNumber))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    try:
        findShop = User.objects.get(Q(Type=2) & Q(UID=findOrder.ShopUID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
    if findOrder.DeliveryState > 1:
        try:
            findDeliveryStaff = User.objects.get(Q(UID=findOrder.DeliveryStaffUID))
        except User.DoesNotExist:
            return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
        return JsonResponse({
            'StatusCode': 200,
            'OrderNumber': findOrder.OrderNumber,
            'Address': findOrder.Address,
            'Phone': findOrder.Phone,
            'Notes': findOrder.Notes,
            'Payment': findOrder.get_Payment_display(),
            'PayStatus': findOrder.PayStatus,
            'ShopName': findShop.Name,
            'ShopAddress': findShop.Address,
            'ShopPhone': findShop.Phone,
            'DeliveryStaffName': findDeliveryStaff.Name,
            'DeliveryStaffPhone': findDeliveryStaff.Phone,
            'DeliveryStatus': findOrder.get_DeliveryState_display(),
            'CartMenber': findOrder.Cart,
            'MoneySum': findOrder.MoneySum
        })
    elif findOrder.DeliveryState==0 or findOrder.DeliveryState==1:
        return JsonResponse({
            'StatusCode': 200,
            'OrderNumber': findOrder.OrderNumber,
            'Address': findOrder.Address,
            'Phone': findOrder.Phone,
            'Notes': findOrder.Notes,
            'Payment': findOrder.get_Payment_display(),
            'PayStatus': findOrder.PayStatus,
            'ShopName': findShop.Name,
            'ShopAddress': findShop.Address,
            'ShopPhone': findShop.Phone,
            'DeliveryStaffName': '',
            'DeliveryStaffPhone': '',
            'DeliveryStatus': findOrder.get_DeliveryState_display(),
            'CartMenber': findOrder.Cart,
            'MoneySum': findOrder.MoneySum
        })
    return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
