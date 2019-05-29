//章节内容号
var contant_id = '0';
//课程号
var course_id = '0';
//章节号
var chapter_id = '0';
//本页面中上次学习的课程号
var pre_course_id = '0';
//本页面中上次学习的章节号
var pre_chapter_id = '0';
//本页面中上次学习的章节内容号
var pre_contant_id = '0';
//用户选择课程的类型，默认为基础课程
var course_type = 'basic';
//代码提交时间控制
var post_time_interval = 10;
//本章课程学习持续时间
var last_time = 0;
window.setInterval(function () {
    last_time++;
    post_time_interval++;
}, 1000);

window.onload = course_getFocus;

//------页面卸载文档时提交本章节学习时长
$(window).bind('beforeunload', function (e) {
    //询问用户是否需要调整页面
    var win = window.event || e;

    //新版本浏览器不支持弹出窗口内容修改，本内容注销
    // var hour = 0;
    // var min = 0;
    // var sec = 0;
    //
    // if (last_time == 0) {
    //    win.returnValue= "亲确定离开当前学习页面吗？";
    // } else {
    //     //计算学习时长，格式化为"XX小时XX分钟XX秒"
    //     hour = Math.floor(last_time / 3600);
    //     min = Math.floor((last_time - hour * 3600) / 60);
    //     sec = last_time - hour * 3600 - min * 60;
    //     var res = '';
    //     if (hour != 0) {
    //         res += hour + '小时';
    //     }
    //     if (min != 0) {
    //         res += min + '分钟';
    //     }
    //     if (sec != 0) {
    //         res += sec + "秒";
    //     }
    //     win.returnValue = ("亲你又学习了" + res + "确定离开当前学习页面吗？");
    // }


    //当页面间切换时进行学习时长插入，重新刷新页面则不进行时间更新
    if (course_id != '0' && chapter_id != '0') {

        //判断课程类型，设置请求路径及发送字段key
        if (course_type == 'basic') {
            var postData = {
                'course_id': course_id,
                'chapter_id': chapter_id,
                'basic_contant_id': contant_id,
                'last_time': last_time
            };
            var url_name = "/basic_learned_time/"
        } else {
            var postData = {
                'course_id': course_id,
                'chapter_id': chapter_id,
                'practice_contant_id': contant_id,
                'last_time': last_time
            };
            var url_name = "/practice_learned_time/"
        }
        $.ajax({
            async: false,
            cache: false,
            type: 'POST',
            url: url_name,
            dataType: "json",
            data: postData,
            error: function () {
                alert('请求失败');
            },
            success: function (data) {
                alert("本次学习时长为" + last_time);
            }
        });
    }
    return win;
});


//------页面加载完成后光标放在滚动条最上层
function course_getFocus() {
    window.scrollTo(0, 0);
}


//------提交后台具体课程号、章节号
function getCont(c) {
//其他课程颜色为白色，被选课程颜色变为黄色
    var allA = document.getElementsByClassName("course");

    for (var i = 0; i < allA.length; i++) {
        allA[i].style.color = 'white';
    }
    c.style.color = 'yellow';

    //通过点击的链接获取课程号、章节号，记录本页面上次点击的课程号、章节号、内容号
    pre_chapter_id = chapter_id;
    pre_course_id = course_id;
    pre_contant_id = contant_id;
    course_id = c.getAttribute('name');
    chapter_id = c.getAttribute('id');
    contant_id = '0';
//如果之前学习了课程，更新课程学习时长，否则不更新学习时长
    if (pre_course_id != '0') {

        //判断课程类型，设置请求路径及发送字段key
        if (course_type == 'basic') {
            var beforeData = {
                'course_id': pre_course_id,
                'chapter_id': pre_chapter_id,
                'basic_contant_id': pre_contant_id,
                'last_time': last_time
            };
            var url_name = "/basic_learned_time/"
        } else {
            var beforeData = {
                'course_id': pre_course_id,
                'chapter_id': pre_chapter_id,
                'practice_contant_id': pre_contant_id,
                'last_time': last_time
            };
            var url_name = "/practice_learned_time/"
        }


        $.ajax({
            async: false,
            cache: false,
            type: 'POST',
            url: url_name,
            dataType: "json",
            data: beforeData,
            error: function () {
                alert('请求失败');
            },
            success: function (data) {
                //计算学习时长，格式化为"XX小时XX分钟XX秒"
                var hour = 0;
                var min = 0;
                var sec = 0;
                hour = Math.floor(last_time / 3600);
                min = Math.floor((last_time - hour * 3600) / 60);
                sec = last_time - hour * 3600 - min * 60;
                var res = '';
                if (hour != 0) {
                    res += hour + '小时';
                }
                if (min != 0) {
                    res += min + '分钟';
                }
                if (sec != 0) {
                    res += sec + "秒";
                }
                alert("恭喜亲，" + "又学习了" + res + "!");
            }

        });
    }


    //通知后台用户选择的课程号、章节号
    //判断课程类型，设置请求路径及发送字段key
    if (course_type == 'basic') {
        var postData = {
            'course_id': course_id,
            'chapter_id': chapter_id,
            'basic_contant_id': contant_id
        };

        var url_name_next = "/basic_course_next/";
    } else {
        var postData = {
            'course_id': course_id,
            'chapter_id': chapter_id,
            'practice_contant_id': contant_id
        };

        var url_name_next = "/practice_course_next/";
    }

    $.ajax({
        async: false,
        cache: false,
        type: 'POST',
        url: url_name_next,
        dataType: "json",
        data: postData,
        error: function () {
            alert('请求失败');
        },
        success: function (data) {
            //将新课程的学习时间重置为0
            last_time = 0;
            //获取后台返回的章节内容号
            contant_id = data.contant_id;
            //创建"课程+章节"的学习提示，并设置其属性
            var content = document.createElement('div');
            content.setAttribute('class', "alert alert-success");
            content.setAttribute('style', "width: 55%;text-align: left;float:left");
            if (course_type == 'basic') {
                content.innerHTML = '下面我们来学习' + data.basic_name + '课程中的' + data.basic_chapter_name;

            } else {
                content.innerHTML = '下面我们来学习' + data.practice_name + '课程中的' + data.practice_chapter_name;

            }

            //将生成的提示内容覆盖之前的课程学习提示
            var course = document.getElementById("course");
            course.innerHTML = '';
            course.appendChild(content);
            content.focus();

            //设置"下一步"按钮可用，可用进行之后课程的学习
            document.getElementById('next').disabled = false;
            document.getElementById('next').setAttribute('style', 'background-color:#82C6E0');

        }

    });
}

//------请求下一句课程
function nextContent(c) {
    //判断课程类型，设置请求路径及发送字段key
    if (course_type == 'basic') {
        var postData = {
            'course_id': course_id,
            'chapter_id': chapter_id,
            'basic_contant_id': contant_id
        };

        var url_name_next = "/basic_course_next/";
    } else {
        var postData = {
            'course_id': course_id,
            'chapter_id': chapter_id,
            'practice_contant_id': contant_id
        };

        var url_name_next = "/practice_course_next/";
    }
    $.ajax({
        async: false,
        cache: false,
        type: 'POST',
        url: url_name_next,
        dataType: "json",
        data: postData,
        error: function () {
            alert('请求失败');
        },
        success: function (data) {
            // $("#result").val(data.output)
            contant_id = data.contant_id;
            var content = document.createElement('div');
            content.setAttribute('class', "alert alert-success");
            content.setAttribute('style', "width: 55%;text-align: left;float:left;word-wrap:break-word");
            if (data.isImg) {
                //<img src="{% static 'img/about.jpg' %}">
                var innerimage = document.createElement('img');
                innerimage.src = data.contant_info;
                content.appendChild(innerimage);
                innerimage.style.width='100%';

            } else {
                var str = data.contant_info;
                var i;
                var result = "";
                var c;
                for (i = 0; i < str.length; i++) {
                    c = str.substr(i, 1);
                    if (c == "\n")
                        result = result + "</br>";
                    else if (c == '\t') {
                        result = result + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;';
                    } else if (c == ' ') {
                        result = result + '&nbsp;';
                    } else if (c != "\r"){
                        result = result + c;
                    }

                }
                content.innerHTML = result;
            }
            var course = document.getElementById("course");
            course.appendChild(content);
            //设置课程对话框定位在最底部
            course.scrollTop = course.scrollHeight;
            //设置窗口定位在顶部
            window.scrollTo(0, 0);
            if (data.input) {
                document.getElementById('next').disabled = true;
                document.getElementById('next').setAttribute('style', 'background-color:grey');
                document.getElementById('submit').disabled = false;
                document.getElementById('submit').style.backgroundColor = '#82C6E0';
                document.getElementById('hint').disabled = false;
                document.getElementById('hint').setAttribute('style', 'background-color:#82C6E0');
                document.getElementById('clear').disabled = false;
                document.getElementById('clear').style.backgroundColor = '#82C6E0';

            } else if (data.last) {
                document.getElementById('next').disabled = true;
                document.getElementById('next').setAttribute('style', 'background-color:grey');
            } else {
                document.getElementById('hint').disabled = true;
                document.getElementById('hint').setAttribute('style', 'background-color:grey');
                document.getElementById('next').disabled = false;
                document.getElementById('next').setAttribute('style', 'background-color:#82C6E0');
                document.getElementById('submit').disabled = true;
                document.getElementById('submit').style.backgroundColor = 'grey';

            }


        }
    });
}

//-----请求提示答案
function askHint(c) {
    //判断课程类型，设置请求路径及发送字段key
    if (course_type == 'basic') {
        var postData = {
            'course_id': course_id,
            'chapter_id': chapter_id,
            'basic_contant_id': contant_id
        };

        var url_name_hint = "/basic_code_hint/";
    } else {
        var postData = {
            'course_id': course_id,
            'chapter_id': chapter_id,
            'practice_contant_id': contant_id
        };

        var url_name_hint = "/practice_code_hint/";
    }
    $.ajax({
        async: false,
        cache: false,
        type: 'POST',
        url: url_name_hint,
        dataType: "json",
        data: postData,
        error: function () {
            alert('请求失败');
        },
        success: function (data) {
            // $("#result").val(data.output)
            contant_id = data.contant_id;
            alert(data.codehint);
        }
    });
}
