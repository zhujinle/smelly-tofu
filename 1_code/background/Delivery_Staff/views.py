from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from databaseManagementLocal.models import User, Order, Menu
from django.db.models import Q, F


def InformationView(request):
    if request.method != 'GET':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        inputUID = request.GET.get('UID', None)
        if inputUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=3))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    return JsonResponse({
        'StatusCode': 200,
        'ShopName': FindUser.UserName,
        'AvatarUrl': '' if FindUser.Avatar.name == '' else FindUser.Avatar.url,
        'MenberStatus': FindUser.get_Member_display(),
        'Phone': FindUser.Phone,
        'HealthCertUrl': '' if FindUser.License.name == '' else FindUser.License.url
    })


def ModifyInformation(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 非POST请求
    if request.method != 'POST':
        return JsonResponse({'ret': 400, 'msg': '不支持该类型http请求'})
    try:  # 处理数据，如果数据被修改不符合加密要求，那就返回418
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputUserName = request.POST.get('UserName', None)
        imputphone = request.POST.get('Phone', None)
        inputAvatar = request.FILES.get('AvatarUrl', None)
        inputHealthCert = request.FILES.get('HealthCertUrl', None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(SecretKey=SecretKey) & Q(UID=inputUID) & Q(Type=3))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    if inputUserName is not None:
        finduser.UserName = inputUserName
    if inputAvatar is not None:
        finduser.Avatar = inputAvatar
    if imputphone is not None:
        finduser.Phone = imputphone
    if inputHealthCert is not None:
        finduser.License = inputHealthCert
    finduser.save()
    return JsonResponse({'StatusCode': 200, 'UserName': finduser.UserName})


def OrderListView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=3) & Q(SecretKey=SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    try:
        FindOrder = Order.objects.filter(Q(DeliveryStaffUID=FindUser.UID)).order_by(F('OrderNumber').desc())
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无订单'})
    FindOrder = list(FindOrder)
    for i in range(len(FindOrder)):
        FindOrder[i] = FindOrder[i].OrderNumber
    return JsonResponse({
        'StatusCode': 200,
        'OrderList': list(FindOrder)
    })


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
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=3) & Q(SecretKey=SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    try:
        findOrder = Order.objects.get(Q(DeliveryStaffUID=FindUser.UID) & Q(OrderNumber=inputOrderNumber))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    try:
        findShop = User.objects.get(Q(UID=findOrder.ShopUID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
    if findOrder.DeliveryState < 2:
        return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
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


def ModifyOrder(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputOrderNumber = request.POST.get('OrderNumber', None)
        inputDeliveryStatus = int(request.POST.get('DeliveryStatus', None))
        if SessionToken is None or inputUID is None or SecretKey is None or inputOrderNumber is None or inputDeliveryStatus is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=3) & Q(SecretKey=SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    try:
        FindOrder = Order.objects.get(Q(DeliveryStaffUID=FindUser.UID) & Q(OrderNumber=inputOrderNumber))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    if inputDeliveryStatus > 5 or inputDeliveryStatus < 1:
        return JsonResponse({'StatusCode': 418})
    FindOrder.DeliveryState = inputDeliveryStatus
    FindOrder.save()
    return JsonResponse({
        'StatusCode': 200,
        'OrderNumber': FindOrder.OrderNumber
    })


def DashboardView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=3) & Q(SecretKey=SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    return JsonResponse({
        'StatusCode': 200,
        'SumMoney': FindUser.MoneySum,
        'DailyMoney': FindUser.MoneyDaily,
        'MonthlyMoney': FindUser.MoneyMonthly,
        'Sumcustomer': FindUser.CustomerSum,
        'DailyCustomerSum': FindUser.CustomerDaily
    })
