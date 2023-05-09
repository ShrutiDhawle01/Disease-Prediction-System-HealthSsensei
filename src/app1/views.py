
# Create your views here.
from typing import Any, Dict
from django.shortcuts import render,redirect, HttpResponse,HttpResponseRedirect
import numpy as np
import pandas as pd
import math
import pickle
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate,login,logout
from django.views.generic.base import TemplateView
from django.shortcuts import render
import openai, os
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.views import View
from dotenv import load_dotenv
from .models import Appointment
load_dotenv()

api_key = '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'
with open("model/heart-disease-prediction-knn-model.pkl", "rb") as f:
     modelone = pickle.load(f)
     print(modelone)

with open("model/model_diabetes.pkl", "rb") as f:
     modeltwo = pickle.load(f)
     print(modeltwo)



class HomeTemplateView(TemplateView):
    template_name = "index.html"


    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject=f"{name} from healthSensei.",
            body= 'Hello {},\n\n{}'.format(name, message),
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )

        email.send()


        messages.success(request, 'Email sent successfully.')
        return redirect('index1')
        #






# def HomePage(request):
#     return render(request, "base.html")



class HomeTemplateView1(TemplateView):
    template_name = "index1.html"
# def HomePage(request):
#     return render(request, "base.html")

def SignupPage(request):
    if request.method=='POST':
        User = get_user_model()
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and Confirm password does not match!")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            # return HttpResponse("User has been Created Successfully")
            return redirect("login")


    return render(request, "signup.html")


class AppointmentTemplateView1(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            phone = mobile,
            request = message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an Appointment, We will email you ASAP!")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView1(TemplateView):
    template_name = "manage-appointments.html"
    login_required = True
    paginate_by = 3

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            "appointments" : appointments,
        })
        return context





def LoginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password = pass1)

        if user is not None:
            login(request, user)
            return redirect('index1')
        else:
            return HttpResponse("Username or password is wrong!")
        
    return render(request, "login.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')

def PredictPage(request):
    return render(request, "predict.html")

def PredictHeartDisease(request):
    return render(request, "heartdisease.html")

def PredictDiabetesDisease(request):
    return render(request, "diabetesdisease.html")


def ChatBot(request):
    chatbot_response = None
    if api_key is not None and request.method =='POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        prompt = user_input + 'and give answers in points'
        response  = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 256,
            temperature = 0.5
        )
        # print(response)
        chatbot_response = response["choices"][0]["text"]
    return render(request, 'main.html', {"response": chatbot_response})


def predictresult(request):
    if request.method == 'POST':
        temp={}
        temp['age'] = int(request.POST['age'])
        temp['sex'] = request.POST.get('sex')
        temp['cp'] = request.POST.get('cpt')
        temp['trestbps'] = int(request.POST['trestbps'])
        temp['chol'] = int(request.POST['chol'])
        temp['fbs'] = request.POST.get('fbs')
        temp['restecg'] = int(request.POST['restecg'])
        temp['thalach'] = int(request.POST['thalach'])
        temp['exang'] = request.POST.get('exang')
        temp['oldpeak'] = float(request.POST['oldpeak'])
        temp['slope'] = request.POST.get('slope')
        temp['ca'] = int(request.POST['ca'])
        temp['thal'] = request.POST.get('thal')
        
        testdata=pd.DataFrame({'x':temp}).transpose()
        scoreval=modelone.predict(testdata)[0]
        print(scoreval)
        return render(request,'predictresult.html',{'result':scoreval})


def predictresultdiab(request):
    if request.method == 'POST':
        temp={}
        Pregnancies = int(request.POST['preg'])
        Glucose = request.POST.get('glu')
        BloodPressure = request.POST.get('bp')
        SkinThickness = int(request.POST['stk'])
        Insulin = int(request.POST['ins'])
        BMI = request.POST.get('bmi')
        DiabetesPedigreeFunction = int(request.POST['dpf'])
        Age = int(request.POST['age'])
        model_diabetes = modeltwo['model']
        scaler_diabetes = modeltwo['scaler'] 
        X = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        X = scaler_diabetes.transform(X)
        diab_prediction = model_diabetes.predict(X)
        return render(request,'predictresult2.html',{'result2':diab_prediction})

