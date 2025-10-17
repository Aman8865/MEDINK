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
    # path('', index, name='index'),  # Default route
    # path('login/', login, name='login'),
    path('index/', index, name='index'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('popupform/', popupform, name='popupform'),
    path('report/<int:id>/', report, name='report'),
    path('user_detail/<int:id>/', user_detail, name='user_detail'),
    path('imagingA/', imagingA, name='imagingA'),
    path('RADS/', RADS, name='RADS'),
    path('', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('invoice/', invoice, name='invoice'),
    path('payment/', payment, name='payment'),
    path('api/patient/<int:id>/download/<str:format>/', download_report, name='download_report'),
    path('api/patient/add/',add_patient, name='add_patient'),
    path('api/patient/<int:id>/update/',update_report, name='update_report'),
    path('api/patient/<int:id>/', get_patient, name='get_patient'),
    path('api/patient/<int:id>/update/', update_report, name='update_report'),
    

    
    
    # path('delete_patient/<int:id>/', delete_patient, name='delete_patient'),
]
    
    # API endpoints
#     path('api/patient/add/', add_patient, name='add_patient'),
#     path('api/patient/<int:id>/', get_patient, name='get_patient'),
#     path('api/patient/<int:id>/update/', update_report, name='update_report'),
#     path('api/patient/<int:id>/delete/', delete_patient, name='delete_patient'),
# ]


