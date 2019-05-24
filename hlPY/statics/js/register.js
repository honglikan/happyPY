$(function () {
    //聚焦失焦input
    $("input[name='username']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("支持中文，字母，数字，'-'，'_'的多种组合");
        }
    })
    $("input[name='age']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("未成年人请由家长注册");
        }
    })
    $("input[name='password']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("建议使用字母、数字和符号两种以上的组合，6-20个字符");
        }
    })
    $("input[name='password2']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("请再次输入密码");
        }
    })
    $("input[name='phone']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("验证完后，该手机将收到最新课程信息");
        }
    })
    $("input[name='email']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("验证完后，你可以使用该邮箱登陆和找回密码");
        }
    })
    $("input[name='identify']").focus(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next().next("div").text("看不清？点击图片更换验证码");
        }
    })
    //input各种判断
    //用户名：
    $("input[name='username']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", '#ccc');
        } else if ($(this).val().length > 0 && $(this).val().length < 4) {
            $(this).parent().next("div").text("长度只能在4-20个字符之间");
            $(this).parent().next("div").css("color", 'red');

        } else if ($(this).val().length >= 4 && !isNaN($(this).val())) {
            $(this).parent().next("div").text("用户名不能为纯数字");
            $(this).parent().next("div").css("color", 'red');
        } else {
//			for(var m = 0; m < stuList.length; m++) {
//				if($(this).val() == stuList[m].name) {
//					$(this).parent().next("div").text("该用户名已被注册");
//					$(this).parent().next("div").css("color", 'red');
//					return;
//				}
//			}
            $(this).parent().next("div").text("");
        }


    })
    $("input[name='age']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", '#ccc');
        } else if ($(this).val().length > 2) {
            $(this).parent().next("div").text("长度只能在2个字符以内");
            $(this).parent().next("div").css("color", 'red');
        } else if($(this).val().match(/[^1-9]/g,'')){
            $(this).parent().next("div").text("年龄只能是正整数");
            $(this).parent().next("div").css("color", 'red');
        }else {
            $(this).parent().next("div").text("");
        }
    })
    //密码
    $("input[name='password']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", '#ccc');
        } else if ($(this).val().length > 0 && $(this).val().length < 6) {
            $(this).parent().next("div").text("长度只能在6-20个字符之间");
            $(this).parent().next("div").css("color", 'red');
        } else {
            $(this).parent().next("div").text("");
        }
    })
    //	确认密码
    $("input[name='password2']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", '#ccc');
        } else if ($(this).val() != $("input[name='password']").val()) {
            $(this).parent().next("div").text("两次密码不相同");
            $(this).parent().next("div").css("color", 'red');
        } else {
            $(this).parent().next("div").text("");
        }
    })
    //	手机号
    $("input[name='phone']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", '#ccc');
        } else if ($(this).val().length != 11) {
            $(this).parent().next("div").text("手机号格式不正确");
            $(this).parent().next("div").css("color", 'red');
        }else if($(this).val().substr(0, 1) != 1 || $(this).val().match(/[^0-9]/g,'')){
            $(this).parent().next("div").text("手机号格式不正确");
            $(this).parent().next("div").css("color", 'red');
        }
        else {
            $(this).parent().next("div").text("");
        }
    })
    $("input[name='email']").blur(function () {
        $(this).maxLength = $(this).length;
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", '#ccc');
        } else if (!$(this).val().match(/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/)) {
            $(this).parent().next("div").text("邮箱格式不正确");
            $(this).parent().next("div").css("color", 'red');
        } else {
            $(this).parent().next("div").text("");
        }
    })
    // 	验证码
    //	 验证码刷新
    function code() {
        var str = "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM";
        var str1 = 0;
        for (var i = 0; i < 4; i++) {
            str1 += str.charAt(Math.floor(Math.random() * 62))
        }
        str1 = str1.substring(1)
        $("#code").text(str1);
    }

    code();
    $("#code").click(code);
    //	验证码验证
    $("input[name='identify']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next().next("div").text("");
            $(this).parent().next().next("div").css("color", '#ccc');
        } else if ($(this).val().toUpperCase() != $("#code").text().toUpperCase()) {
            $(this).parent().next().next("div").text("验证码不正确");
            $(this).parent().next().next("div").css("color", 'red');
        } else {
            $(this).parent().next().next("div").text("");
        }
    })

    //	提交按钮
    $("#submit_btn").click(function (e) {
        // alert($('input').length )
        if ($("input[name='identify']").val().toUpperCase() != $("#code").text().toUpperCase()) {
            $("input[name='identify']").parent().next().next("div").text("验证码不正确");
            $("input[name='identify']").parent().next().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }

        //提交时验证input不能为空
        for (var j = 0; j < 8; j++) {
            if ($('input').eq(j).val().length == 0) {
                $('input').eq(j).focus();
                if (j == 7) {
                    $('input').eq(j).parent().next().next(".tips").text("此处不能为空");
                    $('input').eq(j).parent().next().next(".tips").css("color", 'red');
                    e.preventDefault();
                    return;
                }
                // $(this).parent().next("div").text("此处不能为空");
                // $(this).parent().next("div").css("color", 'red');
                $('input').eq(j).parent().next(".tips").text("此处不能为空");
                $('input').eq(j).parent().next(".tips").css("color", 'red');
                 e.preventDefault();
                return;
                }
    }

        if($("input[name='identify']").val().toUpperCase() != $("#code").text().toUpperCase()) {
            // alert($("#code").text())
            // alert()
            $(this).parent().next().next("div").text("验证码不正确");
            $(this).parent().next().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }
        if ($("input[name='phone']").val().substr(0, 1) != 1 || $("input[name='phone']").val().length != 11 || $("input[name='phone']").val().match(/[^0-9]/g)) {
            $("input[name='phone']").parent().next("div").text("手机号格式不正确");
            $("input[name='phone']").parent().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }
        if ($("input[name='password2']").val() != $("input[name='password']").val()) {
            $(this).parent().next("div").text("两次密码不匹配");
            $(this).parent().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }
        if (!$("input[name='email']").val().match(/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/)) {
            $("input[name='email']").parent().next("div").text("邮箱格式不正确");
            $("input[name='email']").parent().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }
        if ($("input[name='age']").val().length > 2) {
            $("input[name='age']").parent().next("div").text("长度只能在2个字符以内");
            $("input[name='age']").parent().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }
        if($("input[name='age']").val().match(/[^1-9]/g,'')){
            $("input[name='age']").parent().next("div").text("年龄只能是正整数");
            $("input[name='age']").parent().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }





        //协议
        if ($("#xieyi")[0].checked) {
            //向变量stuList数组添加一个数值，数值内部格式Student(name,age,password,phone,email)
            //发送用户信息
            stuList.push(new Student($('input').eq(1).val(), $('input').eq(3).val(), $('input').eq(4).val(), $('input').eq(6).val(),$('input').eq(7).val(),stuList.length + 1));
            localStorage.setItem('stuList', JSON.stringify(stuList));
            alert("注册成功");
            window.open("userlist.html", "_blank");
        } else {
            $("#xieyi").next().next().next(".tips").text("请勾选协议");
            $("#xieyi").next().next().next(".tips").css("color", 'red');
            e.preventDefault();
            return;
        }


    })
})
