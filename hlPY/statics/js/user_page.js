var phonenumber
var course_id
var type
var course_name

$(function () {

    $("#changeinfo").click(function (e) {    //通过“修改信息”这个按钮，将修改信息的表单显示出来
        $("#change").show();    //将form表单信息显示
    })
    $("#changeback").click(function (e) {    //通过“返回”这个按钮将修改信息的表单重置，并隐藏
        document.getElementById("change").reset();
        $("#change").hide();
        e.preventDefault();
    })


    //对修改的信息进行验证
    $("#changeconfirm").click(function (e) {
        if (phonenumber !=$("input[name='phone']").val()){
            if ($("input[name='phone']").val().substr(0, 1) != 1 || $("input[name='phone']").val().length != 11 || $("input[name='phone']").val().match(/[^0-9]/g)) {
                $("input[name='phone']").parent().next("div").text("手机号格式不正确");
                $("input[name='phone']").parent().next("div").css("color", 'red');
            e.preventDefault();
            return;
        }
            return;
        }
        //提交时，判定邮箱格式及内容
        if ($("input[name='email']").val().length == 0) {
            $("input[name='email']").parent().next("div").text("邮箱不能为空");
            $("input[name='email']").parent().next("div").css("color", 'red');
            e.preventDefault();
        } else if (!$("input[name='email']").val().match(/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/)) {
            $("input[name='email']").parent().next("div").text("邮箱格式不正确");
            $("input[name='email']").parent().next("div").css("color", 'red');
            e.preventDefault();
            }
        else {
            $("input[name='email']").parent().next("div").text("");
        }
        //提交时，判定手机格式及内容


        //提交时，判定密码是否一致
        if ($("input[name='password2']").val() != $("input[name='password']").val()) {
            $("input[name='password2']").parent().next("div").text("两次密码不匹配");
            $("input[name='password2']").parent().next("div").css("color", 'red');
            e.preventDefault();
        } else {
            $("input[name='password2']").parent().next("div").text("");
        }


    })

      //当光标移动时，验证手机号的格式
    $("input[name='phone']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", 'red');
        } else if ($(this).val().length != 11) {
            $(this).parent().next("div").text("手机号格式不正确");
            $(this).parent().next("div").css("color", 'red');
        } else {
            $(this).parent().next("div").text("");
        }
    })
    //当光标移动时，验证邮箱的格式
    $("input[name='email']").blur(function () {
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
    //当光标移动时，验证密码的内容及格式
    $("input[name='password']").blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().next("div").text("");
            $(this).parent().next("div").css("color", 'red');
        } else if ($(this).val().length > 0 && $(this).val().length < 6) {
            $(this).parent().next("div").text("长度只能在6-20个字符之间");
            $(this).parent().next("div").css("color", 'red');
        } else {
            $(this).parent().next("div").text("");
        }
    })
        //当光标移动时，验证密码的内容及格式
    $("input[name='password2']").blur(function () {
        if ($(this).val() != $("input[name='password']").val()) {
            $(this).parent().next("div").text("两次密码不匹配");
            $(this).parent().next("div").css("color", 'red');
        } else {
            $(this).parent().next("div").text("");
        }
    })

    $("#finishbutton").click(function (e) {      //通过“已完成课程”这个按钮，将完成课程的表单显示出来
        $("#finishcourse").show();    //将form表单信息显示
    })
    $("#finishback").click(function (e) {    //通过“返回”这个按钮，将完成课程的表单隐藏起来
        $("#finishcourse").hide();
        e.preventDefault();
    })
})
