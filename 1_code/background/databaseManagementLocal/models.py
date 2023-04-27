from django.db import models

# Create your models here.
class Customer(models.Model)
    # 名儿
    name = models.CharField(max_length=20)
    # 联系方式
    phone = models.CharField(max_length=20)
