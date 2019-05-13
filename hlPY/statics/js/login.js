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
