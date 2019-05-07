from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import AbstractUser

class course_python_basic(models.Model):
    basic_id = models.IntegerField(blank=False, unique=True)#课程ID
    basic_name = models.CharField(max_length=255,blank=False)#课程名称
    basic_chapter_id = models.IntegerField(blank=False, unique=True)#课程章节号
    basic_chapter_name = models.CharField(max_length=255,blank=False)#课程章节名称
    basic_contant_id = models.IntegerField(blank=False, unique=True)#课程内容ID
    basic_contant_info = models.CharField(max_length=255,blank=False)#课程内容信息

    class Meta:
        unique_together = ("basic_id","basic_chapter_id","basic_contant_id")


class user_info(AbstractUser):
    user_id = models.AutoField(blank=False,primary_key=True)#用户ID
    # username = models.CharField(max_length=255,blank=False,unique=True)#用户名
    #userpwd = models.CharField(max_length=255,blank=False)#用户密码
    sex = models.CharField(max_length=2)#性别
    age = models.IntegerField(default=20)#年龄
    # mail = models.CharField(max_length=40,blank=False,unique=True)#邮箱
    phone = models.CharField(max_length=11,blank=False,unique=True)#电话号码
    coin = models.IntegerField(default=5000)#积分
    # create_date = models.TimeField(blank=False,default=timezone.now)#用户创建时间
    image = models.CharField(max_length=255)#用户头像存放路径
    # last_date = models.DateTimeField(blank=False,default=create_date)
    env_dir = models.CharField(max_length=255)#编程环境路径


class basic_learn_progress(models.Model):
    progress_id = models.AutoField(blank=False,primary_key=True)#进度ID
    user_id = models.ForeignKey('user_info',to_field='user_id',on_delete='CASCADE',related_name='user_id_basic_learn_progress')#用户ID
    basic_id = models.ForeignKey('course_python_basic',to_field='basic_id',on_delete='CASCADE',related_name='basic_id_basic_learn_progress')#基础课程ID
    basic_chapter_id = models.ForeignKey('course_python_basic', to_field='basic_chapter_id', on_delete='CASCADE',related_name='basic_chapter_id_basic_learn_progress')#基础课程章节号
    learn_status = models.CharField(max_length=2,null=True)#学习状态
    learn_time = models.BigIntegerField(default=0)#学习时长


class course_order(models.Model):
    course_order_id = models.AutoField(blank=False,primary_key=True)
    user_id = models.ForeignKey('user_info',to_field='user_id',on_delete='CASCADE')
    basic_id = models.ForeignKey('course_python_basic',to_field='basic_id',on_delete='CASCADE',related_name='basic_id_course_order')
    basic_chapter_id = models.ForeignKey('course_python_basic',to_field='basic_chapter_id',on_delete='CASCADE',related_name='basic_chapter_id_course_order')
    practice_id = models.ForeignKey('course_python_practice',to_field='practice_id',on_delete='CASCADE',related_name='practice_id_course_order')
    practice_chapter_id = models.ForeignKey('course_python_practice',to_field='practice_chapter_id',on_delete='CASCADE',related_name='practice_chapter_id_course_order')
    course_order_time = models.DateTimeField(blank=False,default=timezone.now)
    course_order_no = models.IntegerField(blank=False)


class course_python_practice(models.Model):
    practice_id = models.IntegerField(blank=False, unique=True)#实战课程编号
    practice_name = models.CharField(max_length=255, blank=False)# 实战课程名称
    practice_chapter_id = models.IntegerField(blank=False, unique=True)#实战课程章节ID
    practice_chapter_name = models.CharField(max_length=255,blank=False)#实战课程章节名称
    practice_info_id = models.IntegerField(blank=False)#实战课程内容编号
    practice_info_contant = models.CharField(max_length=255,blank=False)#实战课程内容信息

    class Meta:
        unique_together = ("practice_id","practice_chapter_id","practice_info_id")


class practice_learn_progress(models.Model):
    progress_id = models.IntegerField(blank=False,primary_key=True)#进度ID
    user_id = models.ForeignKey("user_info",to_field="user_id",on_delete="CASCADE") #实战课程学习用户ID
    practice_id = models.ForeignKey("course_python_practice",to_field="practice_id",on_delete="CASCADE",related_name='practice_id_practice_learn_progress') # 实战课程ID
    practice_chapter_id = models.ForeignKey("course_python_practice",to_field="practice_chapter_id",on_delete="CASCADE",related_name='practice_chapter_id_practice_learn_progress')#实战课程章节ID
    learn_status = models.CharField(max_length=2,null=True)#学习状态
    learn_time = models.BigIntegerField(null=True) #学习时长


class program_env(models.Model):
    user_id = models.ForeignKey("user_info",to_field="user_id",on_delete="CASCADE",parent_link=False,related_name='user_id_program_env')#用户ID
    program_env = models.IntegerField(default=1)#开发环境使用权限


class user_tool(models.Model):
    tool_id = models.IntegerField(blank=False,primary_key=True)#自制软件ID
    tool_name = models.CharField(max_length=255,blank=False)#自制软件名称
    tool_describe = models.CharField(max_length=255,blank=False)#软件描述
    tool_owner_id = models.ForeignKey("user_info",to_field="user_id",on_delete="CASCADE",related_name='user_id_user_tool')#软件归属用户ID
    tool_price = models.IntegerField(blank=False)# 软件售价
    create_date = models.DateTimeField(blank=False,default=timezone.now)#上传日期
    conform_status = models.IntegerField(default=0)#软件审核状态
    save_dir = models.CharField(max_length=255,blank=False)#软件保存路径
    download_num = models.IntegerField(blank=False)#软件下载次数
    conform_date = models.DateTimeField(blank=False)#软件审核通过日期


class user_tool_order(models.Model):
    tool_order_id = models.IntegerField(blank=False,primary_key=True)#自制软件订购ID
    tool_id = models.ForeignKey("user_tool",to_field="tool_id",on_delete="CASCADE",related_name='tool_id_user_tool_order')#自制软件ID
    user_id = models.ForeignKey("user_info",to_field="user_id",on_delete="CASCADE",related_name='user_id_user_tool_order')#订购用户ID
    tool_order_time = models.DateTimeField(blank=False,default=timezone.now)#订购时间
    tool_order_no = models.IntegerField(blank=False) #订单号

admin.site.register(course_python_basic)
admin.site.register(course_python_practice)
admin.site.register(user_info)
admin.site.register(basic_learn_progress)
admin.site.register(practice_learn_progress)
admin.site.register(user_tool_order)
admin.site.register(program_env)
admin.site.register(course_order)
admin.site.register(user_tool)



