"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app1 import  views
from django.urls import path
from app1.views import HomeTemplateView
from app1.views import HomeTemplateView1, AppointmentTemplateView1,ManageAppointmentTemplateView1
from app1.views import ChatBot
from app1.views import PredictPage
from app1.views import PredictHeartDisease
from app1.views import predictresult


urlpatterns = [
    path('admin/',admin.site.urls),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    # path('home/', views.HomePage, name='home'),
    # path('base/', views.HomePage, name='home'), 
    path('',HomeTemplateView1.as_view() , name='index1'),
    path('logout/', views.LogoutPage, name='logout'),
    path('main/', views.ChatBot, name='main'),
    path('predict/', views.PredictPage, name='predict'), 
    path('heartdisease/', views.PredictHeartDisease, name='heartdisease'),
    path('diabetesdisease/', views.PredictDiabetesDisease, name='diabetesdisease'),
    path('predictresult/', views.predictresult,name='predictresult'), 
    path('predictresult2/', views.predictresultdiab, name='predictresult2'),
    path('appointment/',AppointmentTemplateView1.as_view() , name='appointment'),
    path('manage-appointments/',ManageAppointmentTemplateView1.as_view() , name='manage-appointments'),
     
    
] 

