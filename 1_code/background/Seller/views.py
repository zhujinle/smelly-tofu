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
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    return JsonResponse({
        'StatusCode': 200,
        'ShopName': FindUser.Name,
        'AvatarUrl': '' if FindUser.Avatar.name == '' else FindUser.Avatar.url,
        'MenberStatus': FindUser.get_Member_display(),
        'Address': FindUser.Address,
        'Phone': FindUser.Phone,
        'BusinessLicenseUrl': '' if FindUser.License.name == '' else FindUser.License.url
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
        inputShopName = request.POST.get('ShopName', None)
        inputAddress = request.POST.get('Address', None)
        imputphone = request.POST.get('Phone', None)
        inputAvatar = request.FILES.get('AvatarUrl', None)
        inputBusinessLicense = request.FILES.get('BusinessLicenseUrl', None)
        if SessionToken is None or inputUID is None or SecretKey is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        finduser = User.objects.get(Q(SecretKey=SecretKey) & Q(UID=inputUID) & Q(Type=2))
    except User.DoesNotExist:
        return JsonResponse({'StatusCode': 401, 'msg': '无此用户'})
    if inputShopName is not None:
        finduser.Name = inputShopName
    if inputAvatar is not None:
        finduser.Avatar = inputAvatar
    if inputAddress is not None:
        finduser.Address = inputAddress
    if imputphone is not None:
        finduser.Phone = imputphone
    if inputBusinessLicense is not None:
        finduser.License = inputBusinessLicense
    finduser.save()
    return JsonResponse({'StatusCode': 200, 'UserName': finduser.Name})


def MenuView(request):
    if request.method != 'GET':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        inputUID = request.GET.get('UID', None)
        if inputUID is None:
            return JsonResponse({'StatusCode': 418})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    try:
        FindMenu = Menu.objects.filter(Q(ShopID=FindUser)).order_by(F('FoodID').desc())
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
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputFoodPhoto = request.FILES.get('FoodPhoto', None)
        imputMoney = request.POST.get('Money', None)
        inputDiscount = request.POST.get('Discount', None)
        if SessionToken is None or inputUID is None or SecretKey is None or imputMoney is None or inputDiscount is None:
            return JsonResponse({'StatusCode': 418})
        if inputFoodPhoto is None:
            return JsonResponse({'StatusCode': 401, 'msg': '图片不对'})
    except:
        return JsonResponse({'StatusCode': 418})
    try:
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2) & Q(SecretKey=SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    res = Menu.objects.create(ShopID=FindUser,
                               FoodPhoto=inputFoodPhoto,
                               Money=imputMoney,
                               Discount=inputDiscount)
    return JsonResponse({
        'StatusCode': 200, 'FoodID':res.FoodID})

def ModifyMenu(request):
    if request.method != 'POST':
        return JsonResponse({'StatusCode': 400, 'msg': '请求方式错误'})
    try:
        SessionToken = request.POST.get('SessionToken', None)
        inputUID = request.POST.get('UID', None)
        SecretKey = request.POST.get('SecretKey', None)
        inputFoodID = request.POST.get('FoodID', None)
        inputFoodPhoto = request.FILES.get('FoodPhoto', None)
        imputMoney = request.POST.get('Money', None)
        inputDiscount = request.POST.get('Discount', None)
        if SessionToken is None or inputUID is None or SecretKey is None:
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
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2) & Q(SecretKey = SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    return JsonResponse({
        'StatusCode': 200,
        'SumMoney': FindUser.MoneySum,
        'DailyMoney': FindUser.MoneyDaily,
        'MonthlyMoney': FindUser.MoneyMonthly,
        'Sumcustomer': FindUser.CustomerSum,
        'DailyCustomerSum': FindUser.CustomerDaily
    })


def OrderList(request):
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
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2) & Q(SecretKey = SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    try:
        FindOrder = Order.objects.filter(Q(ShopUID=FindUser.UID)).order_by(F('OrderNumber').desc())
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    FindOrder = list(FindOrder)
    for i in range(len(FindOrder)):
        FindOrder[i] = FindOrder[i].OrderNumber
    return JsonResponse({
        'StatusCode': 200,
        'OrderList': list(FindOrder)
    })


def DeliveryStaffList(request):
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
        FindUser = User.objects.get(Q(SecretKey = SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    try:
        FindDeliveryStaff = User.objects.filter(Type=3)
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无可用配送员'})
    if inputUID is not None:
        FindDeliveryStaff = FindDeliveryStaff.filter(UID=inputUID)
    FindDeliveryStaff = list(FindDeliveryStaff)
    for i in range(len(FindDeliveryStaff)):
        FindDeliveryStaff[i] = {'UID': FindDeliveryStaff[i].UID, 'Name': FindDeliveryStaff[i].Name, 'Phone': FindDeliveryStaff[i].Phone, 'Member': FindDeliveryStaff[i].get_Member_display(), 'is_active': FindDeliveryStaff[i].is_active}
    return JsonResponse({
        'StatusCode': 200,
        'UserList': FindDeliveryStaff
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
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2) & Q(SecretKey = SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    try:
        FindDeliveryStaff = User.objects.get(Q(Type=3) & Q(UID=inputDeliveryStaffUID))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此配送员'})
    try:
        FindOrder = Order.objects.get(Q(ShopUID=inputUID) & Q(OrderNumber=inputOrderNumber))
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
        FindUser = User.objects.get(Q(UID=inputUID) & Q(Type=2) & Q(SecretKey = SecretKey))
    except:
        return JsonResponse({'StatusCode': 401, 'msg': '无此店家'})
    try:
        findOrder = Order.objects.get(Q(ShopUID=FindUser.UID) & Q(OrderNumber=inputOrderNumber))
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
            'OrderNumber': findOrder.OrderNumber,
            'Address': findOrder.Address,
            'Phone': findOrder.Phone,
            'Notes': findOrder.Notes,
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
            'OrderNumber': findOrder.OrderNumber,
            'Address': findOrder.Address,
            'Phone': findOrder.Phone,
            'Notes': findOrder.Notes,
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
