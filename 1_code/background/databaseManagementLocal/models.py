from django.db import models

# Create your models here.
class User(models.Model):
    # 名儿
    name = models.CharField(max_length=20)
    # 联系方式
    phone = models.CharField(max_length=20)
    # UID
    UID = models.AutoField()
    # 用户类型标记
    class UserType(models.IntegerChoices):
        Customer = 1
        Seller = 2
        DeliveryStaff = 3
        Admin = 4
    type = models.IntegerField(choices = UserType)
    # 会员等级
    class MenberType(models.IntegerChoices):
        Cu = 1
        Ag = 2
        Au = 3
        diamond = 4
    Member = models.IntegerField(choices = MenberType)
    # 地址
    Address = models.CharField(max_length=100)
    # 日金额，在用户侧定义为日消费金额，商家侧定义为日总收入，配送测定义为日收入，一日一清零
    MoneyMonthly = models.IntegerField(max_length=10)
    # 金额，在用户侧定义为月消费金额，商家侧定义为月总收入，配送测定义为月收入，一月一清零
    MoneyMonthly = models.IntegerField(max_length=10)
    # 总金额
    MoneySum = models.IntegerField(max_length=40)

class Cart(models.Model)
    # UID
    uid = models.ForeignKey('User.uid',on_delete=models.CASCADE,)
