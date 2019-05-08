#-*- coding:utf8 -*-
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import datetime
from hlPY.models import user_info


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
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request,user)
            last_time = datetime.datetime.now()
            user_info.objects.filter(username=username).update(last_login=last_time)
            return HttpResponseRedirect("/")
        else:
            return render(request,"login/login.html",{"retcode": 1, "stderr": "用户名或密码不正确"})
    return render(request, 'login/login.html')







