#-*- coding:utf8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from hlPY.models import user_info,basic_learn_progress,practice_learn_progress,course_python_basic,course_python_practice
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required,permission_required
from hlPY.viewsall import codecompilation
import datetime
import json
from django.db.models.aggregates import Count

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
如果成功que，则跳转至登录页面，对密码进行对称哈市加密'''
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

def test(request):
    return render(request, 'test.html', locals())

def learn(request):
    return render(request, 'learn.html', locals())

'''编程环境获取代码函数，要求必须登录的用户才能跳转'''
@login_required
@csrf_exempt
def testcode(request):
    if request.method == 'POST':
        code = request.POST.get("code")
        print(code)
        result = codecompilation.main(code)
        print(result)
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return render(request,'ide.html',locals())


"""用户信息返回函数，返回用户名、手机号、年龄、性别、邮箱"""


def user_page(request):
    if request.session["user"]:
        username = request.session["user"]  # 获取session用户名
        select_database_username = user_info.objects.values('phone', 'age', 'sex', 'email').filter(username=username)  # 从user_info获取手机、年龄、性别、邮箱
        phone = list(select_database_username)[0]['phone']  # 获取手机号
        replace_key = '****'
        phone = phone[0:3]+replace_key+phone[7:11]
        select_database_username[0]['phone'] = phone  # 手机号脱敏
        select_database_username[0]['username'] = username  # 添加session里的用户名
        basic_course_info = user_page2(username)[0]  # 调用user_page2，添加基础课信息
        practice_course_info = user_page2(username)[1]  # 调用user_page2，添加进阶课信息
        d = {'user_info': list(select_database_username)[0], 'basic_course_info': basic_course_info,
             'practice_course_info': practice_course_info}  # 回传信息
        d = json.dumps(d)  # 回传信息转json
        return HttpResponse(d)


"""课程信息返回函数，返回课程id、课程名、章节数、用户学习进度百分比及详细信息"""


def user_page2(username):
        username = username
        select_database_username = user_info.objects.values('user_id').filter(username=username)
        user_id = list(select_database_username)[0]['user_id']  # 解析获取用户id
        select_database_basic_progress1 = basic_learn_progress.objects.values('basic_id').distinct().filter(user_id=user_id)  # 用户已学习基础课程
        select_database_practice_progress1 = practice_learn_progress.objects.values('practice_id').distinct().filter(user_id=user_id)  # 用户已学习实战课程
        basic_info = []
        practice_info = []
        if select_database_basic_progress1 and not select_database_practice_progress1:
            for i in range(len(list(select_database_basic_progress1))):
                basic_course_info = {}
                basic_id = list(select_database_basic_progress1)[i]["basic_id"]  # 获取基础课程id
                select_database_basic_progress2 = basic_learn_progress.objects.values('basic_chapter_id', 'learn_status').filter(user_id=user_id, learn_status=1,basic_id=basic_id)  # 获取用户已学完的基础课程章节id
                select_database_count_basic_course = course_python_basic.objects.values("basic_name", "basic_chapter_id").filter(basic_id=basic_id)  # 获取全部基础课程名称和章节id
                basic_course_info["basic_course_id"] = list(select_database_basic_progress1)[i]["basic_id"]
                basic_course_info["basic_course_num"] = len(list(select_database_count_basic_course))  # 每个基础课程的章节数
                basic_course_info["rate"] = str(round(len(list(select_database_basic_progress2))/basic_course_info["basic_course_num"]*100,0))+'%'  # 计算并转换用户学习进度百分比
                basic_course_info["basic_course_name"] = list(select_database_count_basic_course)[0]['basic_name']
                basic_course_info["user_progress"] = list(select_database_basic_progress2)  # 已完成的章节数和学习状态
                basic_info.append(basic_course_info)
            return basic_info, practice_info
        if select_database_practice_progress1 and not select_database_basic_progress1:
            for i in range(len(list(select_database_practice_progress1))):
                practice_course_info = {}
                practice_id = list(select_database_practice_progress1)[i]["practice_id"]
                print(practice_id)
                select_database_practice_progress2 = practice_learn_progress.objects.values('practice_chapter_id',
                                                                                      'learn_status').filter(
                    user_id=user_id, learn_status=1, practice_id=practice_id)
                select_database_count_practice_course = course_python_practice.objects.values("practice_name",
                                                                                        "practice_chapter_id").filter(
                    practice_id=practice_id)
                practice_course_info["practice_course_id"] = list(select_database_practice_progress1)[i]["practice_id"]
                practice_course_info["practice_course_num"] = len(list(select_database_count_practice_course))
                practice_course_info["rate"] = str(
                    round(len(list(select_database_practice_progress2)) / practice_course_info["practice_course_num"] * 100,
                          0)) + '%'
                practice_course_info["practice_course_name"] = list(select_database_count_practice_course)[0]['practice_name']
                practice_course_info["user_progress"] = list(select_database_practice_progress2)  # 已完成的章节数和学习状态
                practice_info.append(practice_course_info)
            return basic_info, practice_info
        if select_database_basic_progress1 and select_database_practice_progress1:
            for i in range(len(list(select_database_basic_progress1))):
                basic_course_info = {}
                basic_id = list(select_database_basic_progress1)[i]["basic_id"]
                print(basic_id)
                select_database_basic_progress2 = basic_learn_progress.objects.values('basic_chapter_id','learn_status').filter(user_id=user_id, learn_status=1,basic_id=basic_id)
                select_database_count_basic_course = course_python_basic.objects.values("basic_name","basic_chapter_id").filter(basic_id=basic_id)
                basic_course_info["basic_course_id"] = list(select_database_basic_progress1)[i]["basic_id"]
                basic_course_info["basic_course_num"] = len(list(select_database_count_basic_course))
                basic_course_info["rate"] = str(round(len(list(select_database_basic_progress2))/basic_course_info["basic_course_num"]*100,0))+'%'
                basic_course_info["basic_course_name"] = list(select_database_count_basic_course)[0]['basic_name']
                basic_course_info["user_progress"] = list(select_database_basic_progress2)#已完成的章节数和学习状态
                basic_info.append(basic_course_info)
            for i in range(len(list(select_database_practice_progress1))):
                practice_course_info = {}
                practice_id = list(select_database_practice_progress1)[i]["practice_id"]
                print(practice_id)
                select_database_practice_progress2 = practice_learn_progress.objects.values('practice_chapter_id',
                                                                                            'learn_status').filter(
                    user_id=user_id, learn_status=1, practice_id=practice_id)
                select_database_count_practice_course = course_python_practice.objects.values("practice_name",
                                                                                              "practice_chapter_id").filter(
                    practice_id=practice_id)
                practice_course_info["practice_course_id"] = list(select_database_practice_progress1)[i]["practice_id"]
                practice_course_info["practice_course_num"] = len(list(select_database_count_practice_course))
                practice_course_info["rate"] = str(
                    round(len(list(select_database_practice_progress2)) / practice_course_info[
                        "practice_course_num"] * 100,
                          0)) + '%'
                practice_course_info["practice_course_name"] = list(select_database_count_practice_course)[0][
                    'practice_name']
                practice_course_info["user_progress"] = list(select_database_practice_progress2)  # 已完成的章节数和学习状态
                practice_info.append(practice_course_info)
            return  basic_info, practice_info

