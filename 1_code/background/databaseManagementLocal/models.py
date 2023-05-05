from django.db import models


# Create your models here.
class User(models.Model):
    # UID
    UID = models.AutoField(primary_key=True)
    # Password
    Password = models.CharField(max_length=30, help_text='pwd', blank=False)
    # 名儿
    Name = models.CharField(max_length=20, blank=False)
    # 联系方式
    Phone = models.CharField(max_length=20, blank=False)
    # SecretKey
    SecretKey = models.CharField(max_length=100, blank=False)

    # Avatar
    def user_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'uploads/user_{0}_{1}.jpg'.format(self.UID, filename[0:len(filename)-4])

<<<<<<< Updated upstream
    Avatar = models.ImageField(upload_to=user_directory_path, height_field=300, width_field=300)
=======
    Avatar = models.ImageField(upload_to=user_directory_path,  blank=True)
>>>>>>> Stashed changes
    # 证件，商家侧定义为工商证，配送测定义为健康证
    License = models.ImageField(upload_to=user_directory_path)

    # 用户类型标记
    class UserType(models.IntegerChoices):
        Customer = 1
        Seller = 2
        DeliveryStaff = 3
        Admin = 4

    Type = models.IntegerField(choices=UserType.choices, default=1)

    # 会员等级
    class MemberType(models.IntegerChoices):
        Cu = 1
        Ag = 2
        Au = 3
        Diamond = 4

    Member = models.IntegerField(choices=MemberType.choices, default=1)
    # 地址
    Address = models.CharField(max_length=100, blank=True)
    # 日金额，在用户侧定义为日消费金额，商家侧定义为日总收入，配送测定义为日收入，一日一清零
    MoneyDaily = models.IntegerField(default=0)
    # 金额，在用户侧定义为月消费金额，商家侧定义为月总收入，配送测定义为月收入，一月一清零
    MoneyMonthly = models.IntegerField(default=0)
    # 总金额
    MoneySum = models.IntegerField(default=0)
    # 购物车
    Cart = models.JSONField()


class Menu(models.Model):
    # ShopID
    ShopID = models.ForeignKey('User', to_field='UID', on_delete=models.CASCADE)
    # FoodNumber
    FoodID = models.AutoField(primary_key=True)

    # Photo
    def user_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'uploads/user_{0}_Foods_{1}.jpg'.format(self.ShopID, filename)

    FoodPhoto = models.ImageField(upload_to=user_directory_path)
    # Money
    Money = models.FloatField(max_length=10)
    # Discount
    Discount = models.FloatField(max_length=10)


class Order(models.Model):
    # User UID
    UserUID = models.ForeignKey('User', to_field='UID', on_delete=models.CASCADE)
    # OrderNumber
    OrderNumber = models.AutoField(primary_key=True)
    # 地址
    Address = models.CharField(max_length=100, blank=False)
    # 联系电话
    Phone = models.CharField(max_length=30, blank=False)
    # 备注
    Notes = models.CharField(max_length=500, blank=True)

    # 支付方式
    class PaymentType(models.IntegerChoices):
        Alipay = 1
        Wechat = 2
        Balance = 3

    Payment = models.IntegerField(choices=PaymentType.choices, blank=False)
    # 支付状态
    PayStatus = models.BooleanField(blank=False, default=False)
    # 商店UID
    ShopUID = models.IntegerField(blank=False)
    # 配送员UID
    DeliveryStaffUID = models.IntegerField(blank=True, null=True)

    # 配送状态
    class DeliveryType(models.IntegerChoices):
        NoJieDan = 0
        NoDeliveryStaff = 1
        NoQuCan = 2
        QuCaning = 3
        OnRoad = 4
        Done = 5

    DeliveryState = models.IntegerField(choices=DeliveryType.choices, blank=False, default=0)
    # 订单内容
    Cart = models.JSONField(blank=False)
    # 总金额
    MoneySum = models.FloatField(max_length=10, blank=False)