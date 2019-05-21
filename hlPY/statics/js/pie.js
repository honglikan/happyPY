//通过对后台返回的数据进行遍历，将“课程名称”、“学习进度”等信息展现出啦，并将学习进度用echarts圆形进度条的形式展现
/*思路：
* 1、怎么将django中直接读出的数据例如：{{{{basic_course_info.1.basic_course_name}}}}在javascript中呈现
* 2、首先将在html中用某个div将{{{{basic_course_info.1.basic_course_name}}}}作为它的值
* 3、将这个用django取到div的值读到JavaScript中，例如：var a = $(".rate").eq(i).text()
* 4、再利用循环和echarts实现数据获取和进度表呈现的功能
* 注意：1、因为echarts原因，需要规定循环中呈现进度条的td的大小
* 2、因为此处使用for循环，无法在html中直接对每个循环元素的id进行赋值，因此需要：
* 1）var id = $(".course_name").eq(i).text()取某个将赋给元素id的值
* 2）$(".yuan").eq(i).attr('id', id);对yuan类的第几个元素进行赋值 */


function Abc() {    //在页面加载时就执行的函数，实现方法为使用onload函数：<body  onload="Abc()">

	for (var i = 0; i < $(".rate").length; i++) {
		var a = $(".rate").eq(i).text()
		var  e= parseInt(a);
		// alert(typeof (e));
		// var e = $(".rate").eq(0).text()
		//$(".yuan").eq(i).html($(".rate").eq(i).text())//将rate类的第几个元素的值付给yuan类的第几个的值
		var id = $(".course_name").eq(i).text()
		// var id = $(".course_name").eq(0).text()
		// alert(e);
		// alert(typeof (id));
		// alert(id);
		$(".yuan").eq(i).attr('id', id);
		var Chart4 = echarts.init(document.getElementById(id));
		 // alert(typeof Chart4);
		option = {


			title: {
				show: true,
				text: e+'%',
				x: 'center',
				y: 'center',
				textStyle: {
					fontSize: '10',
					color: 'red',
					fontWeight: 'normal'
				}
			},
			tooltip: {
				trigger: 'item',
				formatter: "{d}%",
				show: false
			},
			legend: {
				orient: 'vertical',
				x: 'left',
				show: false
			},
			series:
				{
					name: '',
					type: 'pie',
					radius: ['65%', '85%'],
					avoidLabelOverlap: true,
					hoverAnimation: false,
					label: {
						normal: {
							show: false,
							position: 'center'
						},
						emphasis: {
							show: false
						}
					},
					labelLine: {
						normal: {
							show: false
						}
					},
					data: [
						{value: e, name: ''},
						{value: 100 - e, name: ''}
					]
				},


		};
		Chart4.setOption(option);

		// }
	}
}



