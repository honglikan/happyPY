#-*- coding:utf8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from hlPY.models import user_info,basic_learn_progress,practice_learn_progress,course_python_basic,course_python_practice
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth import authenticate
import datetime

'''首页'''
def home(request):
    return render(request, 'home.html', locals())


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
            '''将用户信息存入session中，为后续函数识别用户是否为登录状态做准备'''
            request.session['user'] = username
            last_time = datetime.datetime.now()
            user_info.objects.filter(username=username).update(last_login=last_time)
            return render_to_response('login/login.html', {'success': True})
        else:
            return render_to_response("login/login.html",{"error": "用户名或密码错误"})
    return render(request, 'login/login.html')

'''注册页面，验证用户名、手机、邮箱是否重复，如果注册失败，则停留在注册页面并显示失败原因，
如果成功，则跳转至登录页面，对密码进行对称哈市加密'''
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        select_database_username = user_info.objects.filter(username=username)
        select_database_phone = user_info.objects.filter(phone=phone)
        select_database_email = user_info.objects.filter(email=email)
        if select_database_username:
            #return render(request,'login/register.html',{"ERROR":"该用户名已存在"})
            return render_to_response('login/register.html',{'error':"该用户名已存在"})
        else:
            if select_database_phone:
                #return render(request,'login/register.html',{"ERROR":"该手机号已用于注册"})
                return render_to_response('login/register.html', {'error': "该手机号已用于注册"})

            else:
                if select_database_email:
                    #return render(request,'login/register.html',{"ERROR":"该邮箱已用于注册"})
                    return render_to_response('login/register.html',{'error':"该邮箱已用于注册"})
                else:
                    psd = make_password(password)
                    insert_database = user_info(username=username, password=psd, phone=phone, email=email, sex=sex,
                                                age=age,
                                                last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                date_joined=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    insert_database.save()
                    #return render(request,'login/register.html',{"SUCCESS":"注册成功"})
                    return render_to_response('login/register.html',{'success':True})
    return render(request,'login/register.html')


def ide(request):
    return render(request, 'ide.html', locals())


def user_page(request):
    if request.session["username"]:
        username = request.session["user"]
        select_database_username = user_info.objects.filter(username=username)
        user_id = select_database_username[10]
        select_database_basic_progress = basic_learn_progress.objects.get(user_id=user_id)
        select_database_practice_progeress = practice_learn_progress.objects.get(user_id=user_id)
        select_database_count_basic_course = course_python_basic.objects.values('basic_name').annotate(num=Count('basic_name'))
        select_database_count_practice_course = course_python_practice.objects.values('practice_name').annotate(num=Count('practice_name'))
        print(select_database_basic_progress,select_database_practice_progeress,select_database_count_basic_course,select_database_count_practice_course)

        #user_info_display = {"username":username,"sex":select_database_username[12],"email":select_database_username[6],"phone":select_database_username[14],"age":select_database_username[13],"chapter_id":[select_database_basic_userid[3],select_database_practice_userid[3]]}
        #return user_info_display
    #else:
        #return render(request,"login/login.html",locals())
        return render(request,'home.html',locals())