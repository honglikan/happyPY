$(function () {

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
     $("#123").blur(function () {
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
    $("#login_submit_btn").click(function (e) {

            if ($("input[name='logidentify']").val().length == 0) {
                 $("#identifyid").text("此处不能为空");
                $("input[name='logidentify']").parent().next().next("div").css("color", 'red');
                e.preventDefault();
                return;
            } else if ($("input[name='logidentify']").val().toUpperCase() != $("#code").text().toUpperCase()) {
               $("#identifyid").text("验证码不正确");
                $("input[name='logidentify']").parent().next().next("div").css("color", 'red');
                e.preventDefault();
                return;
            } else {
                $("input[name='logidentify']").parent().next().next("div").text("");
            }

    })

})
