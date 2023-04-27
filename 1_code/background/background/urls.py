"""background URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


# 模块的import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/V1/Seller/', include('Seller.urls')),
    path('api/V1/Delivery_Staff/', include('Delivery_Staff.urls')),
    path('api/V1/Dashboard/', include('AdminDashboard.urls')),
    path('api/V1/Customer/', include('Customer.urls')),
    path('api/V1/Admin/', include('AdminDashboard.urls')),
]
