import json

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from databaseManagementLocal.models import User, Order, Menu
from django.db.models import *

def UserCreate(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputName = request.POST.get('Name', None)
        inputPhone = request.POST.get('Phone', None)
        inputPassword = request.POST.get('Password', None)
        password = str(make_password(inputPassword))
        inputType = request.POST.get('Type',1)
        SecretKey = request.POST.get('SecretKey', None)
        if SecretKey is None or inputName is None or inputPhone is None or inputPassword is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    res = User.objects.create(username=inputName,
                              Name=inputName,
                               Phone=inputPhone,
                               password=password,
                               SecretKey=SecretKey,
                              Type = int(inputType))
    return JsonResponse({'StatusCode': 200, 'UID': res.UID})

# Create your views here.
def UserView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        if SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    if inputUID is not None:
        inputUID = int(inputUID)
        FindUser = User.objects.values().filter(UID = inputUID)
    else:
        FindUser = User.objects.values()
    FindUser = list(FindUser)
    for i in range(len(FindUser)):
        FindUser[i] = {'UID': FindUser[i]['UID'], 'LastLogin':FindUser[i]['last_login'], 'is_sctive':FindUser[i]['is_active'], 'Address': FindUser[i]['Address'], 'UserName':FindUser[i]['Name'], 'UserType': '用户' if FindUser[i]['Type'] == 1 else ('入驻商户' if FindUser[i]['Type'] ==2 else ('配送员' if FindUser[i]['Type'] == 3 else '系统管理员'))}
    return JsonResponse({
        'StatusCode': 200,
        'UserList': FindUser
    })


def SingleUserView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputTargetUID = request.POST.get('TargetUserUID', None)
        if SecretKey is None or inputTargetUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputTargetUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    return JsonResponse({
        'StatusCode': 200,
        'UID': FindUser.UID,
        'Name': FindUser.Name,
        'Phone': FindUser.Phone,
        'UserName': FindUser.Name,
        'AvatarUrl': '' if FindUser.Avatar.name == '' else FindUser.Avatar.url,
        'BusinessLicenseUrl' if FindUser.Type == 2 else (
            'HealthCertUrl' if FindUser.Type == 3 else 'License'): '' if FindUser.License.name == '' else FindUser.License.url,
        'UserType': FindUser.get_Type_display(),
        'MenberStatus': FindUser.get_Member_display(),
        'Address': FindUser.Address,
        'MoneySum': FindUser.MoneySum,
        'MoneyDaily': FindUser.MoneyDaily,
        'MoneyMonthly': FindUser.MoneyMonthly,
        'Cart': FindUser.Cart,
        'CustomerDaily': FindUser.CustomerDaily,
        'CustomerSum': FindUser.CustomerSum
    })

def DeleteUser(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SecretKey = request.POST.get('SecretKey', None)
        inputTargetUID = request.POST.get('TargetUserUID', None)
        if SecretKey is None or inputTargetUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(SecretKey=SecretKey) & Q(Type=4))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    try:
        FindUser = User.objects.get(Q(UID=inputTargetUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    FindUser.delete()
    return JsonResponse({'StatusCode': 200})

def DeleteFood(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SecretKey = request.POST.get('SecretKey', None)
        inputTargetUID = request.POST.get('TargetFoodID', None)
        if SecretKey is None or inputTargetUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(SecretKey=SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    try:
        FindFood = Menu.objects.get(Q(FoodID=inputTargetUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此食物'})
    FindFood.delete()
    return JsonResponse({'StatusCode': 200})

def DeleteOrder(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SecretKey = request.POST.get('SecretKey', None)
        inputTargetUID = request.POST.get('TargetUserUID', None)
        if SecretKey is None or inputTargetUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(SecretKey=SecretKey) & Q(Type=4))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    try:
        FindOrder = Order.objects.get(Q(OrderNumber=inputTargetUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    FindOrder.delete()
    return JsonResponse({'StatusCode': 200})

def ModifyUser(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SecretKey = request.POST.get('SecretKey', None)
        inputTargetUID = request.POST.get('TargetUserUID', None)
        inputName = request.POST.get('Name', None)
        inputPhone = request.POST.get('Phone', None)
        inputAvatar = request.FILES.get('Avatar', None)
        inputLicense = request.FILES.get('License', None)
        inputType = request.POST.get('Type', None)
        inputMemberType = request.POST.get('MemberType', None)
        inputAddress = request.POST.get('Address', None)
        inputUserName = request.POST.get('UserName', None)
        inputCart = request.POST.get('Cart', None)
        inputactive = request.POST.get('is_active', None)
        if SecretKey is None or inputTargetUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(UID=inputTargetUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    if inputName is not None:
        finduser.Name = inputName
    if inputPhone is not None:
        finduser.Phone = inputPhone
    if inputAvatar is not None:
        finduser.Avatar = inputAvatar
    if inputLicense is not None:
        finduser.License = inputLicense
    if inputType is not None:
        finduser.Type = inputType
    if inputMemberType is not None:
        finduser.Member = inputMemberType
    if inputAddress is not None:
        finduser.Address = inputAddress
    if inputUserName is not None:
        finduser.Name = inputUserName
    if inputCart is not None:
        finduser.Cart = inputCart
    if inputactive == 'true':
        finduser.is_active = True
    if inputactive == 'false':
        finduser.is_active = False
    finduser.save()
    return JsonResponse({'StatusCode': 200, 'UID': finduser.UID})


def MenuView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        TargetShopUID = request.POST.get('TargetShopUID',None)
        if  SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        if TargetShopUID is None:
            FindMenu = Menu.objects.values().order_by('ShopID','FoodID')
        else:
            FindMenu = Menu.objects.filter(Q(ShopID=TargetShopUID)).order_by(F('FoodID'))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无菜单'})
    FindMenu = list(FindMenu.values())
    return JsonResponse({
        'StatusCode': 200,
        'Menu': FindMenu
    })

def AddMenu (request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        # inputFoodPhoto = request.FILES.get('FoodPhoto', None)
        imputMoney = request.POST.get('Money', None)
        inputDiscount = request.POST.get('Discount', None)
        if inputUID is None or SecretKey is None or imputMoney is None or inputDiscount is None:
            return JsonResponse({'StatusCode': 418})
        # if inputFoodPhoto is None:
        #     return JsonResponse({'StatusCode': 401, 'msg': '图片不对'})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    res = Menu.objects.create(ShopID=FindUser,
                               # FoodPhoto=inputFoodPhoto,
                               Money=imputMoney,
                               Discount=inputDiscount)
    return JsonResponse({
        'StatusCode': 200, 'FoodID':res.FoodID})

def ModifyMenu(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputFoodID = request.POST.get('FoodID', None)
        inputFoodPhoto = request.FILES.get('FoodPhoto', None)
        imputMoney = request.POST.get('Money', None)
        inputDiscount = request.POST.get('Discount', None)
        if inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    try:
        FindMenu = Menu.objects.get(Q(ShopID=FindUser) & Q(FoodID=inputFoodID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此商品'})
    if inputFoodPhoto is not None:
        FindMenu.FoodPhoto = inputFoodPhoto
    if imputMoney is not None:
        FindMenu.Money = imputMoney
    if inputDiscount is not None:
        FindMenu.Discount = inputDiscount
    FindMenu.save()
    return JsonResponse({'StatusCode': 200})

def OrderListView(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        if SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindOrder = Order.objects.values().order_by(F('OrderNumber').desc())
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无订单'})
    if inputUID is not None:
        FindOrder = FindOrder.filter(OrderNumber=inputUID)
        return JsonResponse({
            'StatusCode': 200,
            'OrderList': list(FindOrder)
        })
    FindOrder = list(FindOrder)
    for i in range(len(FindOrder)):
        FindOrder[i] = {'OrderNumber': FindOrder[i]['OrderNumber'], 'UID': FindOrder[i]['UserUID_id'], 'Address': FindOrder[i]['Address'], 'Phone': FindOrder[i]['Phone'], 'Notes': FindOrder[i]['Notes'], 'MoneySum': FindOrder[i]['MoneySum'], 'Cart': FindOrder[i]['Cart']}
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
        SecretKey = request.POST.get('SecretKey', None)
        inputOrderNumber = request.POST.get('OrderNumber', None)
        if SecretKey is None or inputOrderNumber is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        findOrder = Order.objects.get(Q(OrderNumber=inputOrderNumber))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    try:
        findShop = User.objects.get(Q(UID=findOrder.ShopUID))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
    if findOrder.DeliveryState > 1:
        try:
            findDeliveryStaff = User.objects.get(Q(UID=findOrder.DeliveryStaffUID))
        except User.DoesNotExist:
            return JsonResponse({'StatusCode': 401, 'msg': '订单信息错误'})
        return JsonResponse({
            'StatusCode': 200,
            'UserUID': findOrder.UserUID_id,
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
    elif findOrder.DeliveryState == 0 or findOrder.DeliveryState == 1:
        return JsonResponse({
            'StatusCode': 200,
            'UserUID': findOrder.UserUID_id,
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


def ModifyOrder(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SecretKey = request.POST.get('SecretKey', None)
        inputOrderNumber = request.POST.get('OrderNumber',None)
        inputAddress = request.POST.get('Address',None)
        inputPhone = request.POST.get('Phone',None)
        inputNotes = request.POST.get('Notes',None)
        inputPayment = request.POST.get('Payment',None)
        inputPayStatus = request.POST.get('PayStatus',None)
        inputShopUID = request.POST.get('ShopUID',None)
        inputDeliveryStaffUID = request.POST.get('DeliveryStaffUID',None)
        inputDeliveryState = request.POST.get('DeliveryState',None)
        if SecretKey is None or inputOrderNumber is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindOrder = Order.objects.get(Q(OrderNumber=inputOrderNumber))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    if inputAddress is not None:
        FindOrder.Address = inputAddress
    if inputPhone is not None:
        FindOrder.Phone = inputPhone
    if inputNotes is not None:
        FindOrder.Notes = inputNotes
    if inputPayment is not None:
        FindOrder.Payment = inputPayment
    if inputPayStatus is not None:
        FindOrder.PayStatus = inputPayStatus
    if inputShopUID is not None:
        FindOrder.ShopUID = inputShopUID
    if inputDeliveryStaffUID is not None:
        FindOrder.DeliveryStaffUID = inputDeliveryStaffUID
    if inputDeliveryState is not None:
        FindOrder.DeliveryState = inputDeliveryState
    FindOrder.MoneySum = 0.0
    Cart = FindOrder.Cart['CartNember']
    for each in Cart:
        try:
            findfood = Menu.objects.get(Q(ShopID__menu=FindOrder.ShopUID) & Q(FoodID=each['Foodid']))
        except:
            return JsonResponse({'StatusCode': 418, 'FoodID':each['Foodid'], 'msg': '无此食物'})
        FindOrder.MoneySum += findfood.Money*findfood.Discount
    FindOrder.save()
    return JsonResponse({
        'StatusCode': 200,
        'OrderNumber': FindOrder.OrderNumber
    })


def DeliveryPush(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputOrderNumber = request.POST.get('OrderNumber',None)
        inputDeliveryStaffUID = request.POST.get('DeliveryStaffUID',None)
        if SessionToken is None or inputUID is None or SecretKey is None or inputOrderNumber is None or inputDeliveryStaffUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindDeliveryStaff = User.objects.get(Q(Type=3) & Q(UID=inputDeliveryStaffUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    try:
        FindOrder = Order.objects.get(Q(OrderNumber=inputOrderNumber))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此订单'})
    FindOrder.DeliveryState = 2
    FindOrder.DeliveryStaffUID = inputDeliveryStaffUID
    FindDeliveryStaff.CustomerDaily +=1
    FindDeliveryStaff.CustomerSum += 1
    FindDeliveryStaff.MoneyMonthly += 1.5
    FindDeliveryStaff.MoneyDaily +=1.5
    FindDeliveryStaff.MoneySum +=1.5
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
    SumMoney = Order.objects.values().aggregate(Sum('MoneySum'))['MoneySum__sum']
    AvgMoney = Order.objects.values().aggregate(Avg('MoneySum'))['MoneySum__avg']
    MaxMoney = Order.objects.values().aggregate(Max('MoneySum'))['MoneySum__max']
    MinMoney = Order.objects.values().aggregate(Min('MoneySum'))['MoneySum__min']
    DailyMoney = User.objects.filter(Type=2).aggregate(Sum('MoneyDaily'))['MoneyDaily__sum']
    MonthlyMoney = User.objects.filter(Type=2).aggregate(Sum('MoneyMonthly'))['MoneyMonthly__sum']
    DailyCustomer = User.objects.filter(Type=2).aggregate(Sum('CustomerDaily'))['CustomerDaily__sum']
    SumCustomer = User.objects.filter(Type=2).aggregate(Sum('CustomerSum'))['CustomerSum__sum']
    UserCounnt = User.objects.values().count()
    return JsonResponse({
        'StatusCode': 200,
        'SumMoney': SumMoney,
        'AvgMoney': AvgMoney,
        'MaxMoney': MaxMoney,
        'MinMoney': MinMoney,
        'DailyMoney': DailyMoney,
        'MonthlyMoney': MonthlyMoney,
        'DailyCustomer': DailyCustomer,
        'SumCustomer': SumCustomer,
        'UserCounnt': UserCounnt
    })
