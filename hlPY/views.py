# -*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from hlPY.models import user_info, basic_learn_progress, practice_learn_progress, course_python_basic, \
    course_python_practice
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from hlPY.viewsall import codecompilation
import datetime
import json
import os, sys
import happyPY.settings as settings
from django.db.models import Q,Sum
from django.db.models.aggregates import Count,Sum


File = settings.BASE_DIR
File1 = 'hlPY'
File2 = 'results'
File3 = 'hints'

'''首页'''


def home(request):
    return render(request, 'home.html', locals())


'''工具集页面'''
def course(request):
    return render(request, 'course_display.html', locals())


'''登录函数，验证用户名和密码是否正确，如果正确，将用户保存在session中'''


@csrf_exempt
def login(request):
    # redirect_to = request.REQUEST.get('next', '')
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
            auth.login(request, user)
            '''将用户信息存入session中，为后续函数识别用户是否为登录状态做准备'''
            request.session['user'] = username
            last_time = datetime.datetime.now()
            user_info.objects.filter(username=username).update(last_login=last_time)
            return render_to_response('login/login.html', {'success': True})
        else:
            return render_to_response("login/login.html", {"error": "用户名或密码错误"})
    return render(request, 'login/login.html')


'''注册页面，验证用户名、手机、邮箱是否重复，如果注册失败，则停留在注册页面并显示失败原因，
如果成功que，则跳转至登录页面，对密码进行对称哈希加密'''


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


'''进入编程环境页面，要求登录用户才能进入，否则会自动跳转到登录页面'''


@login_required
def ide(request):
    return render(request, 'ide.html', locals())


def test(request):
    return render(request, 'test.html', locals())




'''编程环境获取代码函数，要求必须登录的用户才能跳转'''


@csrf_exempt
def testcode(request):
    if request.method == 'POST':
        # 获取用户输入的代码
        code = request.POST.get("code")
        ## 调用codecompilation.py中的main函数，执行用户输入，并返回结果保存到result
        result = codecompilation.main(code)
        # 将用户代码执行的结果进行json化并返回
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return render(request, 'ide.html', locals())


"""接收user_page2返回用户的课程信息：basic_info和practice_info。并添加至用户信息返回函数——返回当前用户名、手机号、年龄、性别、邮箱"""

def user_page(request):
    if request.session["user"]:
        # 获取session用户名
        username = request.session["user"]
        # 从user_info获取手机、年龄、性别、邮箱
        select_database_username = user_info.objects.values('phone', 'age', 'sex', 'email').filter(username=username)
        phone = list(select_database_username)[0]['phone']
        # 对用户手机进行脱敏处理，格式：133****3333
        replace_key = '****'
        phone = phone[0:3]+replace_key+phone[7:11]
        select_database_username[0]['phone'] = phone
        select_database_username[0]['username'] = username
        # 接收user_page2返回值，添加基础课信息
        if user_page2(username):
            basic_course_info = user_page2(username)[0]
        # 接受user_page2，添加进阶课信息
            practice_course_info = user_page2(username)[1]
            learn_time = user_page2(username)[2]
            list(select_database_username)[0]["learn_time"] = learn_time
        # 回传信息
            d = {'user_info': list(select_database_username)[0], 'basic_course_info': basic_course_info,
             'practice_course_info': practice_course_info}
            print(d)
        #d = json.dumps(d,ensure_ascii=False)  # 回传信息转json
            return render(request, 'user_page.html', d)
        else:
            basic_course_info={}
            #basic_course_info["learn_time"] = 0
            practice_course_info={}
            #practice_course_info["learn_time"] = 0
            list(select_database_username)[0]["learn_time"] = '0'
            d = {'user_info': list(select_database_username)[0], 'basic_course_info': basic_course_info,
             'practice_course_info': practice_course_info}
            return render(request, 'user_page.html',d)


"""课程信息返回函数，返回课程id、课程名、章节数、用户学习进度百分比及学习进度等详细信息至user_page"""

def user_page2(username):
    username = username
    select_database_username = user_info.objects.values('user_id').filter(username=username)
    # 解析获取用户id
    user_id = list(select_database_username)[0]['user_id']
    # 获取用户已学习的基础课程
    select_database_basic_progress1 = basic_learn_progress.objects.values('basic_id').distinct().filter(user_id=user_id)
    # 获取用户已学习的实战课程
    select_database_practice_progress1 = practice_learn_progress.objects.values('practice_id').distinct().filter(user_id=user_id)
    basic_info = []
    practice_info = []
    #对获取的已学习基础、实战课程进行判断，若有基础课程学习进度、无实战课程学习进度
    if select_database_basic_progress1 and not select_database_practice_progress1:
        #对用户已学习的基础课程进度进行循环
        for i in range(len(list(select_database_basic_progress1))):
            basic_course_info = {}
            # 获取基础课程id
            basic_id = list(select_database_basic_progress1)[i]["basic_id"]
            # 获取用户已学完的基础课程章节id、用户学习时长及学习状态, 1为已完成，2为进行中
            select_database_basic_progress2 = basic_learn_progress.objects.values('basic_chapter_id', 'learn_status').filter(user_id=user_id, learn_status=1,basic_id=basic_id)
            # 获取全部基础课程名称和章节id
            select_database_count_basic_course1 = course_python_basic.objects.values("basic_name").filter(basic_id=basic_id)
            select_database_count_basic_course = course_python_basic.objects.values("basic_chapter_id").distinct().filter(basic_id=basic_id)
            #用户分课时长统计
            select_database_basic_course_time = basic_learn_progress.objects.filter(user_id=user_id).values("basic_id").annotate(sum_time=Sum("learn_time"))
            #用户总时长统计
            select_database_learn_time = basic_learn_progress.objects.filter(user_id=user_id).aggregate(sum_time2=Sum("learn_time"))
            # 对返回值basic_course_info进行拼接，包括basic_course_id：基础课程id、basic_course_num：每个基础课程章节数、
            # rate：用户已完成的课程占比、basic_course_name：基础课程名、user_progress：已完成的章节数和学习状态
            basic_id = list(select_database_basic_progress1)[i]["basic_id"]
            basic_course_info["basic_course_id"] = basic_id
            basic_course_info["type"] = "basic"
            basic_course_info["basic_course_num"] = len(list(select_database_count_basic_course))
            basic_course_info["rate"] = str(round(len(list(select_database_basic_progress2))/basic_course_info["basic_course_num"]*100,0))[:-2]+'%'
            basic_course_info["basic_course_name"] = list(select_database_count_basic_course1)[0]['basic_name']
            basic_course_time = list(select_database_basic_course_time)[i]["sum_time"]
            basic_course_time_minute ,basic_course_time_second = divmod(basic_course_time,60)
            basic_course_time_hour,basic_course_time_minute = divmod(basic_course_time_minute,60)
            if basic_course_time_hour == 0:
                if basic_course_time_minute == 0:
                    basic_course_time = str(basic_course_time_second)+"秒"
                else:
                    basic_course_time = str(basic_course_time_minute)+"分钟"+str(basic_course_time_second)+"秒"
            else:
                basic_course_time = str(basic_course_time_hour)+"小时"+str(basic_course_time_minute)+"分钟"+str(basic_course_time_second)+"秒"
            learn_time = select_database_learn_time["sum_time2"]
            learn_time_minute, learn_time_second = divmod(learn_time,60)
            learn_time_hour,learn_time_minute = divmod(learn_time_minute,60)
            if learn_time_hour == 0:
                if learn_time_minute == 0:
                    learn_time = str(learn_time_second)+"秒"
                else:
                    learn_time = str(learn_time_minute)+"分钟" +  str(learn_time_second)+"秒"
            else:
                learn_time = str(learn_time_hour)+"小时"+ str(learn_time_minute)+"分钟" +  str(learn_time_second)+"秒"
            basic_course_info["basic_course_time"] = basic_course_time
            #basic_course_info["learn_time"] = learn_time
            basic_course_info["user_progress"] = list(select_database_basic_progress2)  # 已完成的章节数和学习状态
            basic_info.append(basic_course_info)
        return basic_info, practice_info,learn_time
    #对获取的已学习基础、实战课程进行判断，若有实战课程学习进度、无基础课程学习进度
    if select_database_practice_progress1 and not select_database_basic_progress1:
        # 对用户已学习的实战课程进度进行循环
        for i in range(len(list(select_database_practice_progress1))):
            practice_course_info = {}
            # 获取实战课程id
            practice_id = list(select_database_practice_progress1)[i]["practice_id"]
            # 获取用户已学完的实战课程章节id及学习状态, 1为已完成，2为进行中
            select_database_practice_progress2 = practice_learn_progress.objects.values('practice_chapter_id',
                                                                                  'learn_status').filter(
                user_id=user_id, learn_status=1, practice_id=practice_id)
            # 获取全部实战课程名称和章节id
            select_database_count_practice_course1 = course_python_practice.objects.values("practice_name",
                                                                                   ).filter(
                practice_id=practice_id)
            select_database_count_practice_course = course_python_practice.objects.values("practice_chapter_id").distinct().filter(practice_id=practice_id)
            # 用户分课时长统计
            select_database_practice_course_time = practice_learn_progress.objects.filter(user_id=user_id).values(
                "practice_id").annotate(sum_time=Sum("learn_time"))
            # 用户总时长统计
            select_database_learn_time = practice_learn_progress.objects.filter(user_id=user_id).aggregate(
                sum_time2=Sum("learn_time"))
            # 对返回值practice_course_info进行拼接，包括practice_course_id：实战课程id、practice_course_num：每个实战课程章节数、
            # rate：用户已完成的课程占比、practice_course_name：实战课程名、user_progress：已完成的章节数和学习状态
            practice_course_info["practice_course_id"] = list(select_database_practice_progress1)[i]["practice_id"]
            practice_course_info["type"] = "practice"
            practice_course_info["practice_course_num"] = len(list(select_database_count_practice_course))
            practice_course_time = list(select_database_practice_course_time)[i]["sum_time"]
            practice_course_time_minute, practice_course_time_second = divmod(practice_course_time, 60)
            practice_course_time_hour, practice_course_time_minute = divmod(practice_course_time_minute, 60)
            if practice_course_time_hour == 0:
                if practice_course_time_minute == 0:
                    practice_course_time = str(practice_course_time_second)+"秒"
                else:
                    practice_course_time = str(practice_course_time_minute)+"分钟"+str(practice_course_time_second)+"秒"
            else:
                practice_course_time = str(practice_course_time_hour)+"小时"+str(practice_course_time_minute)+"分钟"+str(practice_course_time_second)+"秒"
            learn_time = select_database_learn_time["sum_time2"]
            learn_time_minute, learn_time_second = divmod(learn_time, 60)
            learn_time_hour, learn_time_minute = divmod(learn_time_minute, 60)
            if learn_time_hour == 0:
                if learn_time_minute == 0:
                    learn_time = str(learn_time_second) + "秒"
                else:
                    learn_time = str(learn_time_minute) + "分钟" + str(learn_time_second) + "秒"
            else:
                learn_time = str(learn_time_hour) + "小时" + str(learn_time_minute) + "分钟" + str(learn_time_second) + "秒"
            practice_course_info["practice_course_time"] = practice_course_time
            #practice_course_info["learn_time"] = learn_time
            practice_course_info["rate"] = str(
                round(len(list(select_database_practice_progress2)) / practice_course_info["practice_course_num"] * 100,
                      0)) + '%'
            practice_course_info["practice_course_name"] = list(select_database_count_practice_course1)[0]['practice_name']
            practice_course_info["user_progress"] = list(select_database_practice_progress2)  # 已完成的章节数和学习状态
            practice_info.append(practice_course_info)
        return basic_info, practice_info,learn_time
    #对获取的已学习基础、实战课程进行判断，若有实战课程学习进度、基础课程学习进度，具体注释参见上文
    if select_database_basic_progress1 and select_database_practice_progress1:
        for i in range(len(list(select_database_basic_progress1))):
            basic_course_info = {}
            # 获取基础课程id
            basic_id = list(select_database_basic_progress1)[i]["basic_id"]
            # 获取用户已学完的基础课程章节id、用户学习时长及学习状态, 1为已完成，2为进行中
            select_database_basic_progress2 = basic_learn_progress.objects.values('basic_chapter_id',
                                                                                  'learn_status').filter(
                user_id=user_id, learn_status=1, basic_id=basic_id)
            # 获取全部基础课程名称和章节id
            select_database_count_basic_course1 = course_python_basic.objects.values("basic_name").filter(
                basic_id=basic_id)
            select_database_count_basic_course = course_python_basic.objects.values(
                "basic_chapter_id").distinct().filter(basic_id=basic_id)
            # 用户分课时长统计
            select_database_basic_course_time = basic_learn_progress.objects.filter(user_id=user_id).values(
                "basic_id").annotate(sum_time=Sum("learn_time"))
            # 用户总时长统计
            select_database_learn_time = basic_learn_progress.objects.filter(user_id=user_id).aggregate(
                sum_time2=Sum("learn_time"))
            # 对返回值basic_course_info进行拼接，包括basic_course_id：基础课程id、basic_course_num：每个基础课程章节数、
            # rate：用户已完成的课程占比、basic_course_name：基础课程名、user_progress：已完成的章节数和学习状态
            basic_id = list(select_database_basic_progress1)[i]["basic_id"]
            basic_course_info["basic_course_id"] = basic_id
            basic_course_info["type"] = "basic"
            basic_course_info["basic_course_num"] = len(list(select_database_count_basic_course))
            basic_course_info["rate"] = str(
                round(len(list(select_database_basic_progress2)) / basic_course_info["basic_course_num"] * 100, 0))[
                                        :-2] + '%'
            basic_course_info["basic_course_name"] = list(select_database_count_basic_course1)[0]['basic_name']
            basic_course_time = list(select_database_basic_course_time)[i]["sum_time"]
            basic_course_time_minute ,basic_course_time_second = divmod(basic_course_time,60)
            basic_course_time_hour,basic_course_time_minute = divmod(basic_course_time_minute,60)
            if basic_course_time_hour == 0:
                if basic_course_time_minute == 0:
                    basic_course_time = str(basic_course_time_second)+"秒"
                else:
                    basic_course_time = str(basic_course_time_minute)+"分钟"+str(basic_course_time_second)+"秒"
            else:
                basic_course_time = str(basic_course_time_hour)+"小时"+str(basic_course_time_minute)+"分钟"+str(basic_course_time_second)+"秒"
            learn_time = select_database_learn_time["sum_time2"]
            basic_course_info["basic_course_time"] = basic_course_time
            #basic_course_info["learn_time"] = learn_time
            basic_course_info["user_progress"] = list(select_database_basic_progress2)  # 已完成的章节数和学习状态
            basic_info.append(basic_course_info)
        for i in range(len(list(select_database_practice_progress1))):
            practice_course_info = {}
            # 获取实战课程id
            practice_id = list(select_database_practice_progress1)[i]["practice_id"]
            # 获取用户已学完的实战课程章节id及学习状态, 1为已完成，2为进行中
            select_database_practice_progress2 = practice_learn_progress.objects.values('practice_chapter_id',
                                                                                        'learn_status').filter(
                user_id=user_id, learn_status=1, practice_id=practice_id)
            # 获取全部实战课程名称和章节id
            select_database_count_practice_course1 = course_python_practice.objects.values("practice_name",
                                                                                           ).filter(
                practice_id=practice_id)
            select_database_count_practice_course = course_python_practice.objects.values(
                "practice_chapter_id").distinct().filter(practice_id=practice_id)
            # 用户分课时长统计
            select_database_practice_course_time = practice_learn_progress.objects.filter(user_id=user_id).values(
                "practice_id").annotate(sum_time=Sum("learn_time"))
            # 用户总时长统计
            select_database_learn_time = practice_learn_progress.objects.filter(user_id=user_id).aggregate(
                sum_time2=Sum("learn_time"))
            # 对返回值practice_course_info进行拼接，包括practice_course_id：实战课程id、practice_course_num：每个实战课程章节数、
            # rate：用户已完成的课程占比、practice_course_name：实战课程名、user_progress：已完成的章节数和学习状态
            practice_course_info["practice_course_id"] = list(select_database_practice_progress1)[i]["practice_id"]
            practice_course_info["practice_course_num"] = len(list(select_database_count_practice_course))
            practice_course_info["type"] = "practice"
            practice_course_time = list(select_database_practice_course_time)[i]["sum_time"]
            practice_course_time_minute, practice_course_time_second = divmod(practice_course_time, 60)
            practice_course_time_hour, practice_course_time_minute = divmod(practice_course_time_minute, 60)
            if practice_course_time_hour == 0:
                if practice_course_time_minute == 0:
                    practice_course_time = str(practice_course_time_second) + "秒"
                else:
                    practice_course_time = str(practice_course_time_minute) + "分钟" + str(
                        practice_course_time_second) + "秒"
            else:
                practice_course_time = str(practice_course_time_hour) + "小时" + str(
                    practice_course_time_minute) + "分钟" + str(practice_course_time_second) + "秒"
            practice_course_info["practice_course_time"] = practice_course_time
            practice_course_info["rate"] = str(
                round(len(list(select_database_practice_progress2)) / practice_course_info["practice_course_num"] * 100,
                      0)) + '%'
            practice_course_info["practice_course_name"] = list(select_database_count_practice_course1)[0][
                'practice_name']
            practice_course_info["user_progress"] = list(select_database_practice_progress2)  # 已完成的章节数和学习状态
            practice_info.append(practice_course_info)
        learn_time1 = basic_learn_progress.objects.filter(user_id=user_id).aggregate(sum_time2=Sum("learn_time"))[
            "sum_time2"]
        learn_time2 = practice_learn_progress.objects.filter(user_id=user_id).aggregate(sum_time2=Sum("learn_time"))[
            "sum_time2"]
        learn_time = learn_time1 + learn_time2
        learn_time_minute, learn_time_second = divmod(learn_time, 60)
        learn_time_hour, learn_time_minute = divmod(learn_time_minute, 60)
        if learn_time_hour == 0:
            if learn_time_minute == 0:
                learn_time = str(learn_time_second) + "秒"
            else:
                learn_time = str(learn_time_minute) + "分钟" + str(learn_time_second) + "秒"
        else:
            learn_time = str(learn_time_hour) + "小时" + str(learn_time_minute) + "分钟" + str(learn_time_second) + "秒"
        return basic_info, practice_info,learn_time


"""用户页用户信息变更，可更改用户密码、手机号、邮箱
读取用户输入，输出更改后的用户信息
"""

@csrf_exempt
def user_info_modify(request):
    if request.session["user"]:
        username = request.session["user"]
        if request.method == 'POST':
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            select_database_phone1 = user_info.objects.values("phone").filter(username=username)
            #前台返回当前用户信息至表单，如用户修改的手机号和邮箱，在数据库中进行查重，若重复返回错误信息；若不重
            select_database_email = user_info.objects.filter(~Q(username=username),email=email)
            if select_database_email:
                return render(request, 'user_page.html', {'error': "该邮箱已用于注册"})
            else:
                if not password:
                    select_database_password = user_info.objects.values("password").filter(username=username)
                    psd = select_database_password[0]['password']
                else:
                    psd = make_password(password)
                if '*' in phone:
                    user_info.objects.filter(username=username).update(password=psd, email=email)
                    return render_to_response('user_page.html', {"success": True})
                else:
                    select_database_phone = user_info.objects.filter(~Q(username=username), phone=phone)
                    if select_database_phone:
                        return render(request,'user_page.html',{'error': "该手机号已用于注册"})
                    user_info.objects.filter(username=username).update(password=psd, phone=phone, email=email)
                    return render_to_response('user_page.html',{"success":True})


"""用户页面跳转学习界面函数，点击相应“继续学习”按钮，将用户页面返回的课程类型、课程id、课程名，传至学习界面，匹配相应导航栏"""
@csrf_exempt
def user_course_locate(request):
    if request.method=='POST':
        continue_course_type = request.POST.get('type', '')
        continue_course_id = request.POST.get('course_id', '')
        continue_course_name = request.POST.get('course_name', '')
        print(continue_course_type, continue_course_id, continue_course_name)
        if continue_course_type=='basic':
            if request.session["user"]:
                username = request.session["user"]
                # 根据session中用户名获取用户id
                select_database_user_id = user_info.objects.values("user_id").filter(username=username)
                user_id = select_database_user_id[0]["user_id"]
                # 根据用户id匹配用户的学习进度
                select_database_learn_progress = basic_learn_progress.objects.values("learn_status", "basic_id",
                                                                                     "basic_chapter_id").filter(
                    user_id=user_id)
                # 获取全量课程id、课程名、章节id、章节名
                select_database_course_name = course_python_basic.objects.values("basic_name", "basic_id",
                                                                                 "basic_chapter_id",
                                                                                 "basic_chapter_name").distinct()
                d = {"basic_info": []}
                progress = []
                progress1 = {}
                # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
                for i in range(len(list(select_database_course_name))):
                    list(select_database_course_name)[i]["learn_status"] = '0'
                # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
                for j in range(len(list(select_database_learn_progress))):
                    for i in range(len(list(select_database_course_name))):
                        if list(select_database_learn_progress)[j]["basic_id"] == list(select_database_course_name)[i][
                            "basic_id"] and list(select_database_learn_progress)[j]["basic_chapter_id"] == \
                                list(select_database_course_name)[i]["basic_chapter_id"]:
                            list(select_database_course_name)[i]["learn_status"] = \
                            list(select_database_learn_progress)[j]["learn_status"]
                # 将拼接后的全量课程表的第一行中basic_chapter_id、basic_chapter_name、learn_status作为progess字典的key-value，
                # 与basic_id、basic_name一起作为初始值加到页面返回值中
                progress1["basic_chapter_name"] = list(select_database_course_name)[0]["basic_chapter_name"]
                progress1["learn_status"] = list(select_database_course_name)[0]["learn_status"]
                progress1["basic_chapter_id"] = list(select_database_course_name)[0]["basic_chapter_id"]
                progress.append(progress1)
                d["basic_info"].append({"basic_name": list(select_database_course_name)[0]["basic_name"],
                                        "basic_id": list(select_database_course_name)[0]["basic_id"],
                                        "progress": progress})
                # 对全量课程表中的第二行开始依此与第一行的basic_id进行比较，如果相同，在第一个progress添加相应字段；
                # 如果不同，在basic_info中添加新的basic_name并添加相应progress字段
                # k用于计数basic_info内list的项
                k = 0
                progress3 = []
                for i in range(1, len(list(select_database_course_name))):
                    if list(select_database_course_name)[i]["basic_name"] == d["basic_info"][0 + k]["basic_name"]:
                        progress2 = {}
                        progress2["basic_chapter_name"] = list(select_database_course_name)[i]["basic_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["basic_chapter_id"] = list(select_database_course_name)[i]["basic_chapter_id"]
                        d["basic_info"][k]["progress"].append(progress2)
                    else:
                        progress2 = {}
                        progress2["basic_chapter_name"] = list(select_database_course_name)[i]["basic_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["basic_chapter_id"] = list(select_database_course_name)[i]["basic_chapter_id"]
                        progress3.append(progress2)
                        d["basic_info"].append({"basic_name": list(select_database_course_name)[i]["basic_name"],
                                                "basic_id": list(select_database_course_name)[i]["basic_id"],
                                                "progress": progress3})
                        k += 1
                d["continue_course_id"] = int(continue_course_id)
                d["continue_course_name"] = continue_course_name
                # return render_to_response("test.html", d)
                #return HttpResponseRedirect('../test')
                return render(request,'learn.html',d)
        if continue_course_type == 'practice':
            if request.session["user"]:
                username = request.session["user"]
                # 根据session中用户名获取用户id
                select_database_user_id = user_info.objects.values("user_id").filter(username=username)
                user_id = select_database_user_id[0]["user_id"]
                # 根据用户id匹配用户的学习进度
                select_database_learn_progress = practice_learn_progress.objects.values("learn_status", "practice_id",
                                                                                        "practice_chapter_id").filter(
                    user_id=user_id)
                # 获取全量课程id、课程名、章节id、章节名
                select_database_course_name = course_python_practice.objects.values("practice_name", "practice_id",
                                                                                    "practice_chapter_id",
                                                                                    "practice_chapter_name").distinct()
                d = {"practice_info": []}
                progress = []
                progress1 = {}
                # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
                for i in range(len(list(select_database_course_name))):
                    list(select_database_course_name)[i]["learn_status"] = '0'
                # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
                for j in range(len(list(select_database_learn_progress))):
                    for i in range(len(list(select_database_course_name))):
                        if list(select_database_learn_progress)[j]["practice_id"] == \
                                list(select_database_course_name)[i]["practice_id"] and \
                                list(select_database_learn_progress)[j]["practice_chapter_id"] == \
                                list(select_database_course_name)[i]["practice_chapter_id"]:
                            list(select_database_course_name)[i]["learn_status"] = \
                            list(select_database_learn_progress)[j]["learn_status"]
                # 将拼接后的全量课程表的第一行中practice_chapter_id、practice_chapter_name、learn_status作为progess字典的key-value，
                # 与practice_id、practice_name一起作为初始值加到页面返回值中
                progress1["practice_chapter_name"] = list(select_database_course_name)[0]["practice_chapter_name"]
                progress1["learn_status"] = list(select_database_course_name)[0]["learn_status"]
                progress1["practice_chapter_id"] = list(select_database_course_name)[0]["practice_chapter_id"]
                progress.append(progress1)
                d["practice_info"].append({"practice_name": list(select_database_course_name)[0]["practice_name"],
                                           "practice_id": list(select_database_course_name)[0]["practice_id"],
                                           "progress": progress})
                # 对全量课程表中的第二行开始依此与第一行的practice_id进行比较，如果相同，在第一个progress添加相应字段；
                # 如果不同，在practice_info中添加新的practice_name并添加相应progress字段
                # k用于计数practice_info内list的项
                k = 0
                progress3 = []
                for i in range(1, len(list(select_database_course_name))):
                    if list(select_database_course_name)[i]["practice_name"] == d["practice_info"][0 + k][
                        "practice_name"]:
                        progress2 = {}
                        progress2["practice_chapter_name"] = list(select_database_course_name)[i][
                            "practice_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["practice_chapter_id"] = list(select_database_course_name)[i]["practice_chapter_id"]
                        d["practice_info"][k]["progress"].append(progress2)
                    else:
                        progress2 = {}
                        progress2["practice_chapter_name"] = list(select_database_course_name)[i][
                            "practice_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["practice_chapter_id"] = list(select_database_course_name)[i]["practice_chapter_id"]
                        progress3.append(progress2)
                        d["practice_info"].append(
                            {"practice_name": list(select_database_course_name)[i]["practice_name"],
                             "practice_id": list(select_database_course_name)[i]["practice_id"], "progress": progress3})
                        k += 1
                d["continue_course_id"] = int(continue_course_id)
                d["continue_course_name"] = continue_course_name
                # return render_to_response("test.html", d)
                return render(request,'learn.html',d)



"""用于返回学习界面左侧导航栏学习状态，获取全量课程及用户学习进度，
返回值:{'basic_info': [
{'basic_name': '123', 'basic_id': 1, 'progress': [{'basic_chapter_name': '123', 'learn_status': '1', 'basic_chapter_id': 1}, 
{'basic_chapter_name': '1234', 'learn_status': '2', 'basic_chapter_id': 2}, 
{'basic_chapter_name': '12345', 'learn_status': 0, 'basic_chapter_id': 3}]}, 
{'basic_name': '234', 'basic_id': 2, 'progress': [{'basic_chapter_name': '234', 'learn_status': '1', 'basic_chapter_id': 1}]}]}
"""

@csrf_exempt
def learn_basic(request):
    if request.session["user"]:
        username = request.session["user"]
        # 根据session中用户名获取用户id
        select_database_user_id = user_info.objects.values("user_id").filter(username=username)
        user_id = select_database_user_id[0]["user_id"]
        # 根据用户id匹配用户的学习进度
        select_database_learn_progress = basic_learn_progress.objects.values("learn_status", "basic_id",
                                                                             "basic_chapter_id").filter(user_id=user_id)
        # 获取全量课程id、课程名、章节id、章节名
        select_database_course_name = course_python_basic.objects.values("basic_name", "basic_id", "basic_chapter_id",
                                                                         "basic_chapter_name").distinct()
        d = {"basic_info": []}
        progress = []
        progress1 = {}
        # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
        for i in range(len(list(select_database_course_name))):
            list(select_database_course_name)[i]["learn_status"] = 0
        # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
        for j in range(len(list(select_database_learn_progress))):
            for i in range(len(list(select_database_course_name))):
                if list(select_database_learn_progress)[j]["basic_id"] == list(select_database_course_name)[i][
                    "basic_id"] and list(select_database_learn_progress)[j]["basic_chapter_id"] == \
                        list(select_database_course_name)[i]["basic_chapter_id"]:
                    list(select_database_course_name)[i]["learn_status"] = list(select_database_learn_progress)[j][
                        "learn_status"]
        # 将拼接后的全量课程表的第一行中basic_chapter_id、basic_chapter_name、learn_status作为progess字典的key-value，
        # 与basic_id、basic_name一起作为初始值加到页面返回值中
        progress1["basic_chapter_name"] = list(select_database_course_name)[0]["basic_chapter_name"]
        progress1["learn_status"] = list(select_database_course_name)[0]["learn_status"]
        progress1["basic_chapter_id"] = list(select_database_course_name)[0]["basic_chapter_id"]
        progress.append(progress1)
        d["basic_info"].append({"basic_name": list(select_database_course_name)[0]["basic_name"],
                                "basic_id": list(select_database_course_name)[0]["basic_id"], "progress": progress})
        # 对全量课程表中的第二行开始依此与第一行的basic_id进行比较，如果相同，在第一个progress添加相应字段；
        # 如果不同，在basic_info中添加新的basic_name并添加相应progress字段
        # k用于计数basic_info内list的项
        k = 0
        progress3 = []
        for i in range(1, len(list(select_database_course_name))):
            if list(select_database_course_name)[i]["basic_name"] == d["basic_info"][0 + k]["basic_name"]:
                progress2 = {}
                progress2["basic_chapter_name"] = list(select_database_course_name)[i]["basic_chapter_name"]
                progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                progress2["basic_chapter_id"] = list(select_database_course_name)[i]["basic_chapter_id"]
                d["basic_info"][k]["progress"].append(progress2)
            else:
                progress2 = {}
                progress2["basic_chapter_name"] = list(select_database_course_name)[i]["basic_chapter_name"]
                progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                progress2["basic_chapter_id"] = list(select_database_course_name)[i]["basic_chapter_id"]
                progress3.append(progress2)
                d["basic_info"].append({"basic_name": list(select_database_course_name)[i]["basic_name"],
                                        "basic_id": list(select_database_course_name)[i]["basic_id"],
                                        "progress": progress3})
                k += 1
        return render(request, "learn.html", d)


"""用于返回学习界面左侧导航栏学习状态，获取全量课程及用户学习进度，
返回值:{'practice_info': [
{'practice_name': '123', 'practice_id': 1, 'progress': [{'practice_chapter_name': '123', 'learn_status': '1', 'practice_chapter_id': 1}, 
{'practice_chapter_name': '1234', 'learn_status': '2', 'practice_chapter_id': 2}, 
{'practice_chapter_name': '12345', 'learn_status': 0, 'practice_chapter_id': 3}]}, 
{'practice_name': '234', 'practice_id': 2, 'progress': [{'practice_chapter_name': '234', 'learn_status': '1', 'practice_chapter_id': 1}]}]}
"""


def learn_practice(request):
    if request.session["user"]:
        username = request.session["user"]
        # 根据session中用户名获取用户id
        select_database_user_id = user_info.objects.values("user_id").filter(username=username)
        user_id = select_database_user_id[0]["user_id"]
        # 根据用户id匹配用户的学习进度
        select_database_learn_progress = practice_learn_progress.objects.values("learn_status", "practice_id",
                                                                                "practice_chapter_id").filter(
            user_id=user_id)
        # 获取全量课程id、课程名、章节id、章节名
        select_database_course_name = course_python_practice.objects.values("practice_name", "practice_id",
                                                                            "practice_chapter_id",
                                                                            "practice_chapter_name").distinct()
        d = {"practice_info": []}
        progress = []
        progress1 = {}
        # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
        for i in range(len(list(select_database_course_name))):
            list(select_database_course_name)[i]["learn_status"] = 0
        # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
        for j in range(len(list(select_database_learn_progress))):
            for i in range(len(list(select_database_course_name))):
                if list(select_database_learn_progress)[j]["practice_id"] == list(select_database_course_name)[i][
                    "practice_id"] and list(select_database_learn_progress)[j]["practice_chapter_id"] == \
                        list(select_database_course_name)[i]["practice_chapter_id"]:
                    list(select_database_course_name)[i]["learn_status"] = list(select_database_learn_progress)[j][
                        "learn_status"]
        # 将拼接后的全量课程表的第一行中practice_chapter_id、practice_chapter_name、learn_status作为progess字典的key-value，
        # 与practice_id、practice_name一起作为初始值加到页面返回值中
        progress1["practice_chapter_name"] = list(select_database_course_name)[0]["practice_chapter_name"]
        progress1["learn_status"] = list(select_database_course_name)[0]["learn_status"]
        progress1["practice_chapter_id"] = list(select_database_course_name)[0]["practice_chapter_id"]
        progress.append(progress1)
        d["practice_info"].append({"practice_name": list(select_database_course_name)[0]["practice_name"],
                                   "practice_id": list(select_database_course_name)[0]["practice_id"],
                                   "progress": progress})
        # 对全量课程表中的第二行开始依此与第一行的practice_id进行比较，如果相同，在第一个progress添加相应字段；
        # 如果不同，在practice_info中添加新的practice_name并添加相应progress字段
        # k用于计数practice_info内list的项
        k = 0
        progress3 = []
        for i in range(1, len(list(select_database_course_name))):
            if list(select_database_course_name)[i]["practice_name"] == d["practice_info"][0 + k]["practice_name"]:
                progress2 = {}
                progress2["practice_chapter_name"] = list(select_database_course_name)[i]["practice_chapter_name"]
                progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                progress2["practice_chapter_id"] = list(select_database_course_name)[i]["practice_chapter_id"]
                d["practice_info"][k]["progress"].append(progress2)
            else:
                progress2 = {}
                progress2["practice_chapter_name"] = list(select_database_course_name)[i]["practice_chapter_name"]
                progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                progress2["practice_chapter_id"] = list(select_database_course_name)[i]["practice_chapter_id"]
                progress3.append(progress2)
                d["practice_info"].append({"practice_name": list(select_database_course_name)[i]["practice_name"],
                                           "practice_id": list(select_database_course_name)[i]["practice_id"],
                                           "progress": progress3})
                k += 1
        return render(request, "learn.html", d)


def learn_page(request):
    return render(request, 'learn.html', locals())


'''用户退出'''


def logout(request):
    auth.logout(request)
    return render(request, 'home.html', locals())


'''基础课程页面，点击'下一步'按钮，触发该函数，根据获取到的课程id，章节id和语句id，
获取语句具体内容，并判断是否最后一句，是否为用户输入，返回是否最后一句的判断，是否为用户输入的判断，
本句话的内容和下一句的语句id'''


@csrf_exempt
def basic_course_next(request):
    if request.method == 'POST':
        # 获取课程id，章节id和语句id
        basic_id_id = request.POST.get('course_id')
        basic_id = int(basic_id_id)
        chapter_id_id = request.POST.get('chapter_id')
        chapter_id = int(chapter_id_id)
        contantid = request.POST.get('basic_contant_id')
        contant_id = int(contantid)
        # 判断语句id是否为0，如果为0，则返回给前端课程名和章节名，以及下一语句的id
        if contant_id == 0:
            # 定义一个字典
            course_contant_info = {}
            # 设置字典course_contant_info的key'content_id'=1
            course_contant_info['contant_id'] = 1
            # 拼接课程id
            contant_id_id = basic_id_id + '_' + chapter_id_id + '_1'
            # 根据课程id，章节id以及语句id，从数据库中取出课程名和章节名
            contant = course_python_basic.objects.values('basic_name', 'basic_chapter_name').filter(basic_id=basic_id,
                                                                                                    basic_chapter_id=chapter_id,
                                                                                                    basic_contant_id=contant_id_id)
            # 设置字典course_contant_info的key'basic_name'和'basic_chapter_name'
            course_contant_info['basic_name'] = contant[0]['basic_name']
            course_contant_info['basic_chapter_name'] = contant[0]['basic_chapter_name']
            '''将字典转化成json格式并返回给前端，返回结果样例为
            {"content_id": 1, "basic_name": "python基础", "basic_chapter_name": "初识python"}'''
            return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
        # 判断语句id是否为0，如果不为0，则返回给前端是否最后一句的判断，是否为用户输入的判断，本句话的内容和下一句的语句id
        else:
            # 定义一个字典
            course_contant_info = {}
            # 根据课程id，章节id，从数据库中取出该章节课程所有的语句，保存在contant_nums中
            contant_nums = course_python_basic.objects.values('basic_contant_id').filter(basic_id=basic_id,
                                                                                         basic_chapter_id=chapter_id)
            # 计算该章节课程语句的总数，保存在contant_num中
            contant_num = len(list(contant_nums))
            #拼接课程id
            contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + contantid
            # 根据课程id，章节id以及语句id，从数据库中取出语句内容，格式为Query格式
            contant = course_python_basic.objects.values('basic_contant_info').filter(basic_id=basic_id,
                                                                                      basic_chapter_id=chapter_id,
                                                                                      basic_contant_id=contant_id_id)
            # contant_info为语句内容
            contant_info = contant[0]['basic_contant_info']
            # 判断是否为最后一句
            # 如果语句id小于语句数量，即还没有到该章节最后一句，则设置字典course_contant_info的key'last'=False
            if contant_id < contant_num:
                course_contant_info['last'] = False
                #判断该句是否为图片
                #如果语句以'Img@'开头，认为其为图片，course_contant_info的key'isImg'=True
                if str(contant_info).startswith('Img@'):
                    course_contant_info['isImg'] = True
                    course_contant_info['input'] = False
                    course_contant_info['contant_id'] = contant_id + 1
                    course_contant_info['contant_info'] = str(contant_info)[4:]
                    '''将字典转化成json格式并返回给前端，返回结果样例为
                {"last": false, "input": true, "content_id": 9, 'isImg':true
                "content_info": ""}'''
                    return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                        content_type="application/json")
                else:
                    course_contant_info['isImg'] = False
                    # 判断是否需要用户输入
                    # 如果语句以'#'开头，认为其为需要用户输入的地方，设置字典course_contant_info的key'input'=True
                    if str(contant_info).startswith('#'):
                        course_contant_info['input'] = True
                        # 设置字典course_contant_info的key'contant_id'=contant_id + 1，即返回下一句的id
                        course_contant_info['contant_id'] = contant_id + 1
                        # 取出该语句的内容,str(contant_info)[1:]表示取出该句除开头'#'之外的语句，存入设置字典course_contant_info的key'contant_info'中
                        course_contant_info['contant_info'] = str(contant_info)[1:]
                        '''将字典转化成json格式并返回给前端，返回结果样例为
                    {"last": false, "input": true, "content_id": 9, 'isImg':false
                    "content_info": "来和小派一起写一个   “轻松快乐学Python,化繁为简so fashion!”"}'''
                        return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                            content_type="application/json")
                    else:
                        # 如果语句不以'#'开头，设置字典course_contant_info的key'input'=False
                        course_contant_info['input'] = False
                        course_contant_info['contant_id'] = contant_id + 1
                        course_contant_info['contant_info'] = contant_info
                        '''将字典转化成json格式并返回给前端，返回结果样例为
                    {"last": false, "input": false, "content_id": 2, "content_info": "大家好，我是小派！感谢大家选择快乐学Python产品，接下来的课程将由我为大家一一介绍，满满的都是知识点呦~"}'''
                        return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                            content_type="application/json")
            else:
                # 如果语句id大于等于语句数量，则设置字典course_contant_info的key'last'=True
                course_contant_info['last'] = True
                course_contant_info['isImg'] = False
                course_contant_info['input'] = False
                course_contant_info['contant_id'] = contant_id
                course_contant_info['contant_info'] = contant_info
                '''将字典转化成json格式并返回给前端，返回结果样例为
                {"last": true, "input": false, "content_id": 18,'isImg':false,
                 "content_info": "当然，我们可以导入的模块有好多好多，随着课程的继续，小派教你一些常用模块^_^，第一节课到此结束。"}'''
                return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                    content_type="application/json")
    return render(request, 'learn.html', locals())


'''实战课程页面，点击'下一步'按钮，触发该函数，根据获取到的课程id，章节id和语句id，
获取语句具体内容，并判断是否最后一句，是否为用户输入，返回是否最后一句的判断，是否为用户输入的判断，
本句话的内容和下一句的语句id'''

@csrf_exempt
def practice_course_next(request):
    if request.method == 'POST':
        # 获取课程id，章节id和语句id
        practice_id_id = request.POST.get('course_id')
        practice_id = int(practice_id_id)
        chapter_id_id = request.POST.get('chapter_id')
        chapter_id = int(chapter_id_id)
        contantid = request.POST.get('practice_contant_id')
        contant_id = int(contantid)
        # 判断语句id是否为0，如果为0，则返回给前端课程名和章节名，以及下一语句的id
        if contant_id == 0:
            # 定义一个字典
            course_contant_info = {}
            # 设置字典course_contant_info的key'content_id'=1
            course_contant_info['contant_id'] = 1
            # 拼接课程id
            contant_id_id = practice_id_id + '_' + chapter_id_id + '_1'
            # 根据课程id，章节id以及语句id，从数据库中取出课程名和章节名
            contant = course_python_practice.objects.values('practice_name', 'practice_chapter_name').filter(practice_id=practice_id,
                                                                                                    practice_chapter_id=chapter_id,
                                                                                                    practice_contant_id=contant_id_id)
            # 设置字典course_contant_info的key'practice_name'和'practice_chapter_name'
            course_contant_info['practice_name'] = contant[0]['practice_name']
            course_contant_info['practice_chapter_name'] = contant[0]['practice_chapter_name']
            '''将字典转化成json格式并返回给前端，返回结果样例为
            {"content_id": 1, "practice_name": "python基础", "practice_chapter_name": "初识python"}'''
            return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
        # 判断语句id是否为0，如果不为0，则返回给前端是否最后一句的判断，是否为用户输入的判断，本句话的内容和下一句的语句id
        else:
            # 定义一个字典
            course_contant_info = {}
            # 根据课程id，章节id，从数据库中取出该章节课程所有的语句，保存在contant_nums中
            contant_nums = course_python_practice.objects.values('practice_contant_id').filter(practice_id=practice_id,
                                                                                         practice_chapter_id=chapter_id)
            # 计算该章节课程语句的总数，保存在contant_num中
            contant_num = len(list(contant_nums))
            #拼接课程id
            contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + contantid
            # 根据课程id，章节id以及语句id，从数据库中取出语句内容，格式为Query格式
            contant = course_python_practice.objects.values('practice_contant_info').filter(practice_id=practice_id,
                                                                                      practice_chapter_id=chapter_id,
                                                                                      practice_contant_id=contant_id_id)
            # contant_info为语句内容
            contant_info = contant[0]['practice_contant_info']
            # 判断是否为最后一句
            # 如果语句id小于语句数量，即还没有到该章节最后一句，则设置字典course_contant_info的key'last'=False
            if contant_id < contant_num:
                course_contant_info['last'] = False
                # 判断是否需要用户输入
                # 如果语句以'#'开头，认为其为需要用户输入的地方，设置字典course_contant_info的key'input'=True
                if str(contant_info).startswith('#'):
                    course_contant_info['input'] = True
                    # 设置字典course_contant_info的key'contant_id'=contant_id + 1，即返回下一句的id
                    course_contant_info['contant_id'] = contant_id + 1
                    # 取出该语句的内容,str(contant_info)[1:]表示取出该句除开头'#'之外的语句，存入设置字典course_contant_info的key'contant_info'中
                    course_contant_info['contant_info'] = str(contant_info)[1:]
                    '''将字典转化成json格式并返回给前端，返回结果样例为
                {"last": false, "input": true, "content_id": 9, "content_info": "来和小派一起写一个   “轻松快乐学Python,化繁为简so fashion!”"}'''
                    return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                        content_type="application/json")
                else:
                    # 如果语句不以'#'开头，设置字典course_contant_info的key'input'=False
                    course_contant_info['input'] = False
                    course_contant_info['contant_id'] = contant_id + 1
                    course_contant_info['contant_info'] = contant_info
                    '''将字典转化成json格式并返回给前端，返回结果样例为
                {"last": false, "input": false, "content_id": 2, "content_info": "大家好，我是小派！感谢大家选择快乐学Python产品，接下来的课程将由我为大家一一介绍，满满的都是知识点呦~"}'''
                    return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                        content_type="application/json")
            else:
                # 如果语句id大于等于语句数量，则设置字典course_contant_info的key'last'=True
                course_contant_info['last'] = True
                course_contant_info['input'] = False
                course_contant_info['contant_id'] = contant_id
                course_contant_info['contant_info'] = contant_info
                '''将字典转化成json格式并返回给前端，返回结果样例为
                {"last": true, "input": false, "content_id": 18,
                 "content_info": "当然，我们可以导入的模块有好多好多，随着课程的继续，小派教你一些常用模块^_^，第一节课到此结束。"}'''
                return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                    content_type="application/json")
    return render(request, 'learn.html', locals())



'''
def basic_course_post(request):
    if request.method == 'POST':
        course_contant_info = {}
        basic_id = 1
        chapter_id = 1
        contant_id = 1
        code = request.POST.get("code")
        # print(code)
        user_result = codecompilation.main(code)
        filename = str(basic_id) + '_' + str(chapter_id) + '_' + str(contant_id) + '.txt'
        fpath = os.path.join(File, File1, File2, filename)
        with open(fpath, 'r', encoding='utf-8') as f:
            result = f.read()
            if result != user_result:
                contant = course_python_basic.objects.values('basic_contant_info').filter(basic_id=basic_id,
                                                                                          basic_chapter_id=chapter_id,
                                                                                          basic_contant_id=contant_id)
                contant_info = contant[0]['basic_contant_info']
                course_contant_info['content_id'] = contant_id
                course_contant_info['content_info'] = contant_info
                course_contant_info['result'] = user_result
                return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                    content_type="application/json")
            else:
                contant = course_python_basic.objects.values('basic_contant_info').filter(basic_id=basic_id,
                                                                                          basic_chapter_id=chapter_id,
                                                                                          basic_contant_id=contant_id + 1)
                contant_info = contant[0]['basic_contant_info']
                course_contant_info['content_id'] = contant_id + 1
                course_contant_info['content_info'] = contant_info
                course_contant_info['result'] = user_result
                return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False),
                                    content_type="application/json")

    return render(request, 'learn.html', locals())

'''

'''基础课程页面，点击'提交'按钮，触发该函数，根据获取到的课程id，章节id，语句id和代码，
验证用户输入是否正确，并返回对应的语句id，语句信息和用户输入的结果
'''


@csrf_exempt
def basic_course_post(request):
    if request.method == 'POST':
        course_contant_info = {}
        basic_id_id = request.POST.get('course_id')
        basic_id = int(basic_id_id)
        chapter_id_id = request.POST.get('chapter_id')
        chapter_id = int(chapter_id_id)
        contantid = request.POST.get('basic_contant_id')
        contant_id = int(contantid)
        # code用户输入的代码
        code = request.POST.get("code")
        # 调用codecompilation.py中的main函数，执行用户输入，并返回结果保存到user_result
        user_result = codecompilation.main(code)
        # filename为课程id_章节id_语句id.txt
        filename = basic_id_id + '_' + chapter_id_id + '_' + contantid + '.txt'
        # 拼接课程答案保存路径
        fpath = os.path.join(File, File1, File2, filename)
        # 调用codecompilation.py中的correct函数，执行答案，并返回结果保存到result
        result = codecompilation.correct(fpath)
        # 判断用户输入的答案和正确答案是否一样
        # 如果不一样
        if result != user_result:
            contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + contantid
            # 提取用户输入错误时返回的语句信息
            contant = course_python_basic.objects.values('basic_contant_info').filter(basic_id=basic_id,
                                                                                      basic_chapter_id=chapter_id,
                                                                                      basic_contant_id=contant_id_id)
            contant_info = contant[0]['basic_contant_info']
            # 因为输入错误，所以语句id不加1，直接返回
            course_contant_info['contant_id'] = contant_id
            course_contant_info['contant_info'] = contant_info
            course_contant_info['success'] = False
            course_contant_info['result'] = user_result
            '''将字典转化成json格式并返回给前端，返回结果样例为
          {"content_id": 9, "content_info": "有点问题哦，再试一试吧！", "success": false, "result": {"version": "python 3.6", "output": "0\r\n", "code": "Success"}}'''
            return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
        else:
            contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + str(contant_id+1)
            # 提取用户输入正确时返回的语句信息，此时语句id加1
            contant = course_python_basic.objects.values('basic_contant_info').filter(basic_id=basic_id,
                                                                                      basic_chapter_id=chapter_id,
                                                                                      basic_contant_id=contant_id_id)
            contant_info = contant[0]['basic_contant_info']
            # 因为输入正确，所以语句id加1，然后返回
            course_contant_info['contant_id'] = contant_id + 2
            course_contant_info['contant_info'] = contant_info
            course_contant_info['success'] = True
            course_contant_info['result'] = user_result
            '''将字典转化成json格式并返回给前端，返回结果样例为
            {"content_id": 10, "content_info": "哇，你好厉害！这么快就学会了呢！", "success": true, "result": {"version": "python 3.6", "output": "0\r\n1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n", "code": "Success"}}'''
            return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
    return render(request, 'learn.html', locals())


'''实战课程页面，点击'提交'按钮，触发该函数，根据获取到的课程id，章节id，语句id和代码，
验证用户输入是否正确，并返回对应的语句id，语句信息和用户输入的结果
'''

@csrf_exempt
def practice_course_post(request):
    if request.method == 'POST':
        course_contant_info = {}
        practice_id_id = request.POST.get('course_id')
        practice_id = int(practice_id_id)
        chapter_id_id = request.POST.get('chapter_id')
        chapter_id = int(chapter_id_id)
        contantid = request.POST.get('practice_contant_id')
        contant_id = int(contantid)
        # code用户输入的代码
        code = request.POST.get("code")
        # 调用codecompilation.py中的main函数，执行用户输入，并返回结果保存到user_result
        user_result = codecompilation.main(code)
        # filename为课程id_章节id_语句id.txt
        filename = practice_id_id + '_' + chapter_id_id + '_' + contantid + '.txt'
        # 拼接课程答案保存路径
        fpath = os.path.join(File, File1, File2, filename)
        # 调用codecompilation.py中的correct函数，执行答案，并返回结果保存到result
        result = codecompilation.correct(fpath)
        # 判断用户输入的答案和正确答案是否一样
        # 如果不一样
        if result != user_result:
            contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + contantid
            # 提取用户输入错误时返回的语句信息
            contant = course_python_practice.objects.values('practice_contant_info').filter(practice_id=practice_id,
                                                                                      practice_chapter_id=chapter_id,
                                                                                      practice_contant_id=contant_id_id)
            contant_info = contant[0]['practice_contant_info']
            # 因为输入错误，所以语句id不加1，直接返回
            course_contant_info['contant_id'] = contant_id
            course_contant_info['contant_info'] = contant_info
            course_contant_info['success'] = False
            course_contant_info['result'] = user_result
            '''将字典转化成json格式并返回给前端，返回结果样例为
          {"content_id": 9, "content_info": "有点问题哦，再试一试吧！", "success": false, "result": {"version": "python 3.6", "output": "0\r\n", "code": "Success"}}'''
            return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
        else:
            contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + str(contant_id+1)
            # 提取用户输入正确时返回的语句信息，此时语句id加1
            contant = course_python_practice.objects.values('practice_contant_info').filter(practice_id=practice_id,
                                                                                      practice_chapter_id=chapter_id,
                                                                                      practice_contant_id=contant_id_id)
            contant_info = contant[0]['practice_contant_info']
            # 因为输入正确，所以语句id加1，然后返回
            course_contant_info['contant_id'] = contant_id + 1
            course_contant_info['contant_info'] = contant_info
            course_contant_info['success'] = True
            course_contant_info['result'] = user_result
            '''将字典转化成json格式并返回给前端，返回结果样例为
            {"content_id": 10, "content_info": "哇，你好厉害！这么快就学会了呢！", "success": true, "result": {"version": "python 3.6", "output": "0\r\n1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n", "code": "Success"}}'''
            return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
    return render(request, 'learn.html', locals())


'''基础课程页面，点击'提示'按钮，触发该函数，根据获取到的课程id，章节id和语句id，
验证用户输入是否正确，并返回对应的语句id，语句信息和用户输入的结果
'''


@csrf_exempt
def basic_course_hint(request):
    if request.method == 'POST':
        course_contant_info = {}
        basic_id_id = request.POST.get('course_id')
        basic_id = int(basic_id_id)
        chapter_id_id = request.POST.get('chapter_id')
        chapter_id = int(chapter_id_id)
        contantid = request.POST.get('basic_contant_id')
        contant_id = int(contantid)
        # filename为课程id_章节id_语句id.txt
        filename = basic_id_id + '_' + chapter_id_id + '_' + contantid + '.txt'
        # 拼接课程答案保存路径
        fpath = os.path.join(File, File1, File3, filename)
        # 读取答案，保存在hint中
        with open(fpath, 'r', encoding='gbk') as f:
            hint = f.read()
        course_contant_info['codehint'] = hint
        course_contant_info['contant_id'] = contant_id
        '''将字典转化成json格式并返回给前端，返回结果样例为
        {"codehint": "for i in range(10):\n    print(i)"}   '''
        return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
    return render(request, 'learn.html', locals())


'''实战课程页面，点击'提示'按钮，触发该函数，根据获取到的课程id，章节id和语句id，
验证用户输入是否正确，并返回对应的语句id，语句信息和用户输入的结果
'''


@csrf_exempt
def practice_course_hint(request):
    if request.method == 'POST':
        course_contant_info = {}
        practice_id_id = request.POST.get('course_id')
        practice_id = int(practice_id_id)
        chapter_id_id = request.POST.get('chapter_id')
        chapter_id = int(chapter_id_id)
        contantid = request.POST.get('practice_contant_id')
        contant_id = int(contantid)
        # filename为课程id_章节id_语句id.txt
        filename = practice_id_id + '_' + chapter_id_id + '_' + contantid + '.txt'
        # 拼接课程答案保存路径
        fpath = os.path.join(File, File1, File2, filename)
        # 读取答案，保存在hint中
        with open(fpath, 'r', encoding='utf-8') as f:
            hint = f.read()
        course_contant_info['codehint'] = hint
        course_contant_info['contant_id'] = contant_id
        '''将字典转化成json格式并返回给前端，返回结果样例为
        {"codehint": "for i in range(10):\n    print(i)"}   '''
        return HttpResponse(json.dumps(course_contant_info, ensure_ascii=False), content_type="application/json")
    return render(request, 'learn.html', locals())


'''统计用户学习时长函数，根据获取到的课程id，章节id，语句id和学习时长以及session中的用户名，
在数据库表basic_learn_progress中更新该章节，该用户的学习时长'''

@csrf_exempt
def basic_learned_time(request):
    if request.method == 'POST':
        if request.session["user"]:
            #从session中获取用户名
            username = request.session["user"]
            # 通过用户名从user_info获取id
            select_id = user_info.objects.values('user_id').filter(username=username)
            user_id = select_id[0]['user_id']
            #获取课程id，章节id，语句id和学习时长
            basic_id_id = request.POST.get('course_id')
            basic_id = int(basic_id_id)
            chapter_id_id = request.POST.get('chapter_id')
            chapter_id = int(chapter_id_id)
            contantid = request.POST.get('basic_contant_id')
            contant_id = int(contantid)
            last_time = int(request.POST.get('last_time'))
            # 根据课程id，章节id，从数据库中取出该章节课程所有的语句，保存在contant_nums中
            contant_nums = course_python_basic.objects.values('basic_contant_id').filter(basic_id=basic_id,
                                                                                         basic_chapter_id=chapter_id)
            # 计算该章节课程语句的总数，保存在contant_num中
            contant_num = len(list(contant_nums))
            #如果在进度表中没有该用户针对课程该章节的学习记录，则插入一条
            if not basic_learn_progress.objects.filter(basic_id=basic_id, basic_chapter_id=chapter_id, user_id_id=user_id):
                #如果没有学完该章节所有语句，则学习状态记为2，语句插入学完的语句号
                if contant_id < contant_num:
                    #拼接语句id
                    contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + contantid
                    # 学习状态，1：已完成，2：进行中，插入数据库
                    insert_progress = basic_learn_progress(basic_id=basic_id, basic_chapter_id=chapter_id, learn_status='2',
                                                           learn_time=last_time, basic_contant_id_id=contant_id_id,
                                                           user_id_id=user_id)
                    insert_progress.save()
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                # 如果学完该章节所有语句，则学习状态记为1，语句插入最后一句的id
                else:
                    #拼接最后一句的id
                    contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + str(contant_num)
                    insert_progress = basic_learn_progress(basic_id=basic_id, basic_chapter_id=chapter_id, learn_status='1',
                                                           learn_time=last_time, basic_contant_id_id=contant_id_id,
                                                           user_id_id=user_id)
                    insert_progress.save()
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
            # 如果在进度表中有该用户针对课程该章节的学习记录，则更新该条记录
            else:
                #根据用户id，课程和章节提取学习状态、是从和语句id
                select_info = basic_learn_progress.objects.values('learn_status', 'learn_time',
                                                                  'basic_contant_id_id').filter(
                    basic_id=basic_id,
                    basic_chapter_id=chapter_id, user_id_id=user_id)
                learn_status = select_info[0]['learn_status']
                learn_time = select_info[0]['learn_time']
                #由于id是1_1_1格式，需要拆分，并且转换成int格式
                basic_contant_id = int((select_info[0]['basic_contant_id_id']).split('_')[2])
                time = learn_time + last_time
                #如果已完成，则只更新学习时长
                if learn_status == '1':
                    basic_learn_progress.objects.filter(basic_id=basic_id, basic_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time)
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                #如果未完成，则判断当前语句id和数据库语句id
                #如果当前语句id小于数据库语句id
                elif contant_id <= basic_contant_id:
                    #更新学习时长
                    basic_learn_progress.objects.filter(basic_id=basic_id, basic_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time, learn_status='2')
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                #否则，如果当前语句id小于总语句数
                elif contant_id < contant_num:
                    contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + contantid
                    #更新学习时长和学完的语句id
                    basic_learn_progress.objects.filter(basic_id=basic_id, basic_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time, learn_status='2', basic_contant_id_id=contant_id_id)
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                else:
                    contant_id_id = basic_id_id + '_' + chapter_id_id + '_' + str(contant_num)
                    # 更新学习时长和学完的语句id置为最后一句的id
                    basic_learn_progress.objects.filter(basic_id=basic_id, basic_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time, learn_status='1', basic_contant_id_id=contant_id_id)
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")

    return render(request, 'learn.html', locals())



'''统计用户学习时长函数，根据获取到的课程id，章节id，语句id和学习时长以及session中的用户名，
在数据库表practice_learn_progress中更新该章节，该用户的学习时长'''

@csrf_exempt
def practice_learned_time(request):
    if request.method == 'POST':
        if request.session["user"]:
            #从session中获取用户名
            username = request.session["user"]
            # 通过用户名从user_info获取id
            select_id = user_info.objects.values('user_id').filter(username=username)
            user_id = select_id[0]['user_id']
            #获取课程id，章节id，语句id和学习时长
            practice_id_id = request.POST.get('course_id')
            practice_id = int(practice_id_id)
            chapter_id_id = request.POST.get('chapter_id')
            chapter_id = int(chapter_id_id)
            contantid = request.POST.get('practice_contant_id')
            contant_id = int(contantid)
            last_time = int(request.POST.get('last_time'))
            # 根据课程id，章节id，从数据库中取出该章节课程所有的语句，保存在contant_nums中
            contant_nums = course_python_practice.objects.values('practice_contant_id').filter(practice_id=practice_id,
                                                                                         practice_chapter_id=chapter_id)
            # 计算该章节课程语句的总数，保存在contant_num中
            contant_num = len(list(contant_nums))
            #如果在进度表中没有该用户针对课程该章节的学习记录，则插入一条
            if not practice_learn_progress.objects.filter(practice_id=practice_id, practice_chapter_id=chapter_id, user_id_id=user_id):
                #如果没有学完该章节所有语句，则学习状态记为2，语句插入学完的语句号
                if contant_id < contant_num:
                    #拼接语句id
                    contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + contantid
                    # 学习状态，1：已完成，2：进行中，插入数据库
                    insert_progress = practice_learn_progress(practice_id=practice_id, practice_chapter_id=chapter_id, learn_status='2',
                                                           learn_time=last_time, practice_contant_id_id=contant_id_id,
                                                           user_id_id=user_id)
                    insert_progress.save()
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                # 如果学完该章节所有语句，则学习状态记为1，语句插入最后一句的id
                else:
                    #拼接最后一句的id
                    contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + str(contant_num)
                    insert_progress = practice_learn_progress(practice_id=practice_id, practice_chapter_id=chapter_id, learn_status='1',
                                                           learn_time=last_time, practice_contant_id_id=contant_id_id,
                                                           user_id_id=user_id)
                    insert_progress.save()
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
            # 如果在进度表中有该用户针对课程该章节的学习记录，则更新该条记录
            else:
                #根据用户id，课程和章节提取学习状态、是从和语句id
                select_info = practice_learn_progress.objects.values('learn_status', 'learn_time',
                                                                  'practice_contant_id_id').filter(
                    practice_id=practice_id,
                    practice_chapter_id=chapter_id, user_id_id=user_id)
                learn_status = select_info[0]['learn_status']
                learn_time = select_info[0]['learn_time']
                #由于id是1_1_1格式，需要拆分，并且转换成int格式
                practice_contant_id = int((select_info[0]['practice_contant_id_id']).split('_')[2])
                time = learn_time + last_time
                #如果已完成，则只更新学习时长
                if learn_status == '1':
                    practice_learn_progress.objects.filter(practice_id=practice_id, practice_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time)
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                #如果未完成，则判断当前语句id和数据库语句id
                #如果当前语句id小于数据库语句id
                elif contant_id <= practice_contant_id:
                    #更新学习时长
                    practice_learn_progress.objects.filter(practice_id=practice_id, practice_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time, learn_status='2')
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                #否则，如果当前语句id小于总语句数
                elif contant_id < contant_num:
                    contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + contantid
                    #更新学习时长和学完的语句id
                    practice_learn_progress.objects.filter(practice_id=practice_id, practice_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time, learn_status='2', practice_contant_id_id=contant_id_id)
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
                else:
                    contant_id_id = practice_id_id + '_' + chapter_id_id + '_' + str(contant_num)
                    # 更新学习时长和学完的语句id置为最后一句的id
                    practice_learn_progress.objects.filter(practice_id=practice_id, practice_chapter_id=chapter_id,
                                                        user_id_id=user_id).update(
                        learn_time=time, learn_status='1', practice_contant_id_id=contant_id_id)
                    result = {'success': True}
                    return HttpResponse(json.dumps(result), content_type="application/json")
    return render(request, 'learn.html', locals())


def continue_baic_learn1(request):
    if request.method == 'POST':
        if request.session["user"]:
            # 从session中获取用户名
            username = request.session["user"]
            # 通过用户名从user_info获取id
            select_id = user_info.objects.values('user_id').filter(username=username)
            user_id = select_id[0]['user_id']
            # 获取课程id，章节id，语句id和学习时长
            learn_id_id = request.POST.get('course_id')
            learn_id = int(learn_id_id)
            course_type = request.POST.get('type')
            if course_type == 'basic':
                # 根据用户id匹配用户的学习进度
                select_database_learn_progress = basic_learn_progress.objects.values("learn_status", "basic_id",
                                                                                     "basic_chapter_id").filter(
                    user_id=user_id)
                # 获取全量课程id、课程名、章节id、章节名
                select_database_course_name = course_python_basic.objects.values("basic_name", "basic_id",
                                                                                 "basic_chapter_id",
                                                                                 "basic_chapter_name").distinct()
                d = {"basic_info": []}
                progress = []
                progress1 = {}
                # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
                for i in range(len(list(select_database_course_name))):
                    list(select_database_course_name)[i]["learn_status"] = 0
                # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
                for j in range(len(list(select_database_learn_progress))):
                    for i in range(len(list(select_database_course_name))):
                        if list(select_database_learn_progress)[j]["basic_id"] == list(select_database_course_name)[i][
                            "basic_id"] and list(select_database_learn_progress)[j]["basic_chapter_id"] == \
                                list(select_database_course_name)[i]["basic_chapter_id"]:
                            list(select_database_course_name)[i]["learn_status"] = list(select_database_learn_progress)[j][
                                "learn_status"]
                # 将拼接后的全量课程表的第一行中basic_chapter_id、basic_chapter_name、learn_status作为progess字典的key-value，
                # 与basic_id、basic_name一起作为初始值加到页面返回值中
                progress1["basic_chapter_name"] = list(select_database_course_name)[0]["basic_chapter_name"]
                progress1["learn_status"] = list(select_database_course_name)[0]["learn_status"]
                progress1["basic_chapter_id"] = list(select_database_course_name)[0]["basic_chapter_id"]
                progress.append(progress1)
                d["basic_info"].append({"basic_name": list(select_database_course_name)[0]["basic_name"],
                                        "basic_id": list(select_database_course_name)[0]["basic_id"], "progress": progress})
                # 对全量课程表中的第二行开始依此与第一行的basic_id进行比较，如果相同，在第一个progress添加相应字段；
                # 如果不同，在basic_info中添加新的basic_name并添加相应progress字段
                # k用于计数basic_info内list的项
                k = 0
                progress3 = []
                for i in range(1, len(list(select_database_course_name))):
                    if list(select_database_course_name)[i]["basic_name"] == d["basic_info"][0 + k]["basic_name"]:
                        progress2 = {}
                        progress2["basic_chapter_name"] = list(select_database_course_name)[i]["basic_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["basic_chapter_id"] = list(select_database_course_name)[i]["basic_chapter_id"]
                        d["basic_info"][k]["progress"].append(progress2)
                    else:
                        progress2 = {}
                        progress2["basic_chapter_name"] = list(select_database_course_name)[i]["basic_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["basic_chapter_id"] = list(select_database_course_name)[i]["basic_chapter_id"]
                        progress3.append(progress2)
                        d["basic_info"].append({"basic_name": list(select_database_course_name)[i]["basic_name"],
                                                "basic_id": list(select_database_course_name)[i]["basic_id"],
                                                "progress": progress3})
                        k += 1

                chapter_id = 1
                contant_id_id = str(learn_id) + '_1_1'
                select_basic_value = course_python_basic.objects.values("basic_name").filter(
                    basic_id=learn_id, basic_chapter_id=chapter_id, basic_contant_id=contant_id_id)
                basic_name = select_basic_value[0]['basic_name']
                d["basic_id"] = learn_id
                d["basic_name"] = basic_name
            else:
                select_database_learn_progress = practice_learn_progress.objects.values("learn_status", "practice_id",
                                                                                        "practice_chapter_id").filter(
                    user_id=user_id)
                # 获取全量课程id、课程名、章节id、章节名
                select_database_course_name = course_python_practice.objects.values("practice_name", "practice_id",
                                                                                    "practice_chapter_id",
                                                                                    "practice_chapter_name").distinct()
                d = {"practice_info": []}
                progress = []
                progress1 = {}
                # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
                for i in range(len(list(select_database_course_name))):
                    list(select_database_course_name)[i]["learn_status"] = 0
                # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
                for j in range(len(list(select_database_learn_progress))):
                    for i in range(len(list(select_database_course_name))):
                        if list(select_database_learn_progress)[j]["practice_id"] == \
                                list(select_database_course_name)[i][
                                    "practice_id"] and list(select_database_learn_progress)[j]["practice_chapter_id"] == \
                                list(select_database_course_name)[i]["practice_chapter_id"]:
                            list(select_database_course_name)[i]["learn_status"] = \
                            list(select_database_learn_progress)[j][
                                "learn_status"]
                # 将拼接后的全量课程表的第一行中practice_chapter_id、practice_chapter_name、learn_status作为progess字典的key-value，
                # 与practice_id、practice_name一起作为初始值加到页面返回值中
                progress1["practice_chapter_name"] = list(select_database_course_name)[0]["practice_chapter_name"]
                progress1["learn_status"] = list(select_database_course_name)[0]["learn_status"]
                progress1["practice_chapter_id"] = list(select_database_course_name)[0]["practice_chapter_id"]
                progress.append(progress1)
                d["practice_info"].append({"practice_name": list(select_database_course_name)[0]["practice_name"],
                                           "practice_id": list(select_database_course_name)[0]["practice_id"],
                                           "progress": progress})
                # 对全量课程表中的第二行开始依此与第一行的practice_id进行比较，如果相同，在第一个progress添加相应字段；
                # 如果不同，在practice_info中添加新的practice_name并添加相应progress字段
                # k用于计数practice_info内list的项
                k = 0
                progress3 = []
                for i in range(1, len(list(select_database_course_name))):
                    if list(select_database_course_name)[i]["practice_name"] == d["practice_info"][0 + k][
                        "practice_name"]:
                        progress2 = {}
                        progress2["practice_chapter_name"] = list(select_database_course_name)[i][
                            "practice_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["practice_chapter_id"] = list(select_database_course_name)[i]["practice_chapter_id"]
                        d["practice_info"][k]["progress"].append(progress2)
                    else:
                        progress2 = {}
                        progress2["practice_chapter_name"] = list(select_database_course_name)[i][
                            "practice_chapter_name"]
                        progress2["learn_status"] = list(select_database_course_name)[i]["learn_status"]
                        progress2["practice_chapter_id"] = list(select_database_course_name)[i]["practice_chapter_id"]
                        progress3.append(progress2)
                        d["practice_info"].append(
                            {"practice_name": list(select_database_course_name)[i]["practice_name"],
                             "practice_id": list(select_database_course_name)[i]["practice_id"],
                             "progress": progress3})
                        k += 1
                chapter_id = 1
                contant_id_id = str(learn_id) + '_1_1'
                select_practice_value = course_python_practice.objects.values("practice_name").filter(
                    practice_id=learn_id, practice_chapter_id=chapter_id, basic_contant_id=contant_id_id)
                practice_name = select_practice_value[0]['practice_name']
                d["practice_id"] = learn_id
                d["practice_name"] = practice_name
                return render(request, "continue_learn.html", d)



