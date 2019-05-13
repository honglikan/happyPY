#-*- coding:utf8 -*-
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import datetime
from hlPY.models import user_info
from hlPY.viewsall import captcha


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


'''后台验证验证码'''
@csrf_exempt
def login1(request):
    #redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        identify = request.POST.get('identify', '')
        captcha_text = captcha.get_captcha_text()
        if identify == captcha_text:
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
        else:
            return render(request, "login/login.html", {"eror": "验证码输入有误，请重新输入！"})
    return render(request, 'login/login.html')
