"""
URL configuration for medink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from med.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login,name='login'),
    # path('',home,name='home'),
    path('index/', index, name='index'),
    path('profile/',profile,name='profile'),
    path('signup/',signup,name='signup'),
    path('popupform/',popupform,name='popupform'),
    path('report/<int:id>/',report,name='report'),
    path('user_detail/',user_detail,name='user_detail'),
    path('imagingA/',imagingA,name='imagingA'),
    
]
