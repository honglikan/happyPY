"""happyPY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from hlPY import views
from django.urls import path,include,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('ide/',views.ide,name='ide'),
    path('testcode/',views.testcode,name='testcode'),
    path('user_page/', views.user_page, name='user_page'),
    path('',include('django.contrib.auth.urls')),
    path('basic_course_next/',views.basic_course_next,name='basic_course_next'),
    path('practice_course_next/',views.practice_course_next,name='practice_course_next'),
    path('basic_course_codetest/',views.basic_course_post,name='basic_course_codetest'),
    path('practice_course_codetest/',views.practice_course_post,name='practice_course_codetest'),
    path('basic_code_hint/',views.basic_course_hint,name='basic_code_hint'),
    path('practice_code_hint/',views.practice_course_hint,name='practice_course_hint'),
    path('basic_learned_time/',views.basic_learned_time,name='basic_learned_time'),
    path('practice_learned_time/',views.practice_learned_time,name='practice_learned_time'),
    path('learn_basic/',views.learn_basic,name='learn_basic'),
    path('learn_practice/',views.learn_practice,name='learn_practice'),
    path('course/',views.course,name='course'),
    path('user_info_modify/', views.user_info_modify, name='user_info_modify'),
    path('user_course_locate/', views.user_course_locate, name='user_course_locate'),


    #path('basic_course_post/',views.basic_course_post,name='basic_course_post'),
]
