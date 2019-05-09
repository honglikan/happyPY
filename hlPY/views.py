#-*- coding:utf8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hlPY.models import user_info
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth import authenticate
import datetime

def judgeUsername(request):  # 判断注册页面用户名是否重复
    if request.method == 'POST':
        response_result = {'username': ''}
        username = request.POST.get('username')
        response_username = user_info.objects.get(username=username)
        if not response_username:
            response_result['username'] = '0'
            return response_result
        else:
            response_result['username'] = '1'
            return response_result


def judgePhone(request):  # 判断注册页面手机号是否重复
    response_result = {'phone': ''}
    if request.method == 'POST':
        phone = request.POST.get('phone')
        response_phone = user_info.objects.get(phone=phone)
        if not response_phone:
            response_result['phone'] = '0'
            return response_result
        else:
            response_result['phone'] = '1'
            return response_result


def judgeMail(request):  # 判断注册页面邮箱是否重复
    response_result = {'mail': ''}
    if request.method == 'POST':
        mail = request.POST.get('mail')
        response_mail = user_info.objects.get(mail=mail)
        if not response_mail:
            response_result['mail'] = '0'
            return response_result
        else:
            response_result['mail'] = '1'
            return response_result


def home(request):
    return render(request, 'home.html', locals())


'''登录函数，验证用户用户名和密码是否正确，如果正确，跳转到主页，如果不正确，则还停在登录页，并返回错误信息'''
@csrf_exempt
def login(request):
    #redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        '''
               user = user_info.objects.get(username=username)
               if user and user.password == password:
                   auth.login(request, user)
                   last_time = datetime.datetime.now()
                   user_info.objects.filter(username=username).update(last_login=last_time)
                   return HttpResponseRedirect("/")
               '''
        try:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request,user)
                '''从数据库中取出该用户的信息'''
                User = user_info.objects.get(username=username)
                '''将用户信息存入session中，为后续函数识别用户是否为登录状态做准备'''
                request.session['user'] = User
                last_time = datetime.datetime.now()
                user_info.objects.filter(username=username).update(last_login=last_time)
                return HttpResponseRedirect("/")
            else:
                return render(request,"login/login.html",{"eror": "用户名或密码错误"})
        except user_info.DoesNotExist:
            pass
    return render(request, 'login/login.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        psd = make_password(password)
        insert_database = user_info(username=username, password=psd, phone=phone, email=email, sex=sex, age=age,last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,date_joined=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
        insert_database.save()
        return HttpResponseRedirect("/login")
    return render(request,'login/register.html')


def ide(request):
    return render(request, 'ide.html', locals())