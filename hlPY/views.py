from django.shortcuts import render
# Create your views here.
#import hlPY.viewsall.login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hlPY.models import user_info
from django.views.decorators.csrf import csrf_exempt
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


def login(request):
    return render(request, 'login/login.html', locals())


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        insert_database = user_info(username=username, password=password, phone=phone, email=email, sex=sex, age=age,last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,date_joined=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
        insert_database.save()
        return HttpResponseRedirect("/login")
    return render(request,'login/register.html')


def ide(request):
    return render(request, 'ide.html', locals())