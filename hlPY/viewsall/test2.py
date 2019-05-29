def course(request):
    course_id = 1
    course_type = 'practice'
    if request.session["user"]:
        # 从session中获取用户名
        username = request.session["user"]
        # 通过用户名从user_info获取id
        select_id = user_info.objects.values('user_id').filter(username=username)
        user_id = select_id[0]['user_id']
        if course_type == 'basic':
            # 根据用户id匹配用户的学习进度
            select_progress = basic_learn_progress.objects.values("learn_status", "basic_id",
                                                                  "basic_chapter_id").filter(
                user_id=user_id)
            # 通过课程id获取课程名、章节id、章节名
            select_course = course_python_basic.objects.values("basic_name", "basic_id","basic_chapter_id",
                                                               "basic_chapter_name").filter(
                basic_id=course_id).distinct()
            d = {"basic_info": []}
            progress = []
            progress1 = {}
            # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
            for i in range(len(list(select_course))):
                list(select_course)[i]["learn_status"] = 0
            # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
            for j in range(len(list(select_progress))):
                for i in range(len(list(select_course))):
                    if list(select_progress)[j]["basic_id"] == list(select_course)[i][
                        "basic_id"] and list(select_progress)[j]["basic_chapter_id"] == \
                            list(select_course)[i]["basic_chapter_id"]:
                        list(select_course)[i]["learn_status"] = list(select_progress)[j][
                            "learn_status"]
            # 将拼接后的全量课程表的第一行中basic_chapter_id、basic_chapter_name、learn_status作为progess字典的key-value，
            # 与basic_id、basic_name一起作为初始值加到页面返回值中
            progress1["basic_chapter_name"] = list(select_course)[0]["basic_chapter_name"]
            progress1["learn_status"] = list(select_course)[0]["learn_status"]
            progress1["basic_chapter_id"] = list(select_course)[0]["basic_chapter_id"]
            progress.append(progress1)
            d["basic_info"].append({"basic_name": list(select_course)[0]["basic_name"],
                                    "basic_id": list(select_course)[0]["basic_id"], "progress": progress})
            # 对全量课程表中的第二行开始依此与第一行的basic_id进行比较，如果相同，在第一个progress添加相应字段；
            # 如果不同，在basic_info中添加新的basic_name并添加相应progress字段
            # k用于计数basic_info内list的项
            k = 0
            progress3 = []
            for i in range(1, len(list(select_course))):
                if list(select_course)[i]["basic_name"] == d["basic_info"][0 + k]["basic_name"]:
                    progress2 = {}
                    progress2["basic_chapter_name"] = list(select_course)[i]["basic_chapter_name"]
                    progress2["learn_status"] = list(select_course)[i]["learn_status"]
                    progress2["basic_chapter_id"] = list(select_course)[i]["basic_chapter_id"]
                    d["basic_info"][k]["progress"].append(progress2)
                else:
                    progress2 = {}
                    progress2["basic_chapter_name"] = list(select_course)[i]["basic_chapter_name"]
                    progress2["learn_status"] = list(select_course)[i]["learn_status"]
                    progress2["basic_chapter_id"] = list(select_course)[i]["basic_chapter_id"]
                    progress3.append(progress2)
                    d["basic_info"].append({"basic_name": list(select_course)[i]["basic_name"],
                                            "basic_id": list(select_course)[i]["basic_id"],
                                            "progress": progress3})
                    k += 1
        else:
            select_progress = practice_learn_progress.objects.values("learn_status", "practice_id",
                                                                                    "practice_chapter_id").filter(
                user_id=user_id)
            # 通过课程id，获取课程名、章节id、章节名
            select_course = course_python_practice.objects.values("practice_name","practice_id",
                                                                                "practice_chapter_id",
                                                                                "practice_chapter_name").filter(
                practice_id=course_id).distinct()
            d = {"practice_info": []}
            progress = []
            progress1 = {}
            # 将学习进度字段添加到全量课程表中，初始化为0(未学习状态)
            for i in range(len(list(select_course))):
                list(select_course)[i]["learn_status"] = 0
            # 将用户学习进度表映射至全量课程表中，更新学习状态(1为已完成，2为学习中)
            for j in range(len(list(select_progress))):
                for i in range(len(list(select_course))):
                    if list(select_progress)[j]["practice_id"] == \
                            list(select_course)[i][
                                "practice_id"] and list(select_progress)[j]["practice_chapter_id"] == \
                            list(select_course)[i]["practice_chapter_id"]:
                        list(select_course)[i]["learn_status"] = \
                            list(select_progress)[j][
                                "learn_status"]
            # 将拼接后的全量课程表的第一行中practice_chapter_id、practice_chapter_name、learn_status作为progess字典的key-value，
            # 与practice_id、practice_name一起作为初始值加到页面返回值中
            progress1["practice_chapter_name"] = list(select_course)[0]["practice_chapter_name"]
            progress1["learn_status"] = list(select_course)[0]["learn_status"]
            progress1["practice_chapter_id"] = list(select_course)[0]["practice_chapter_id"]
            progress.append(progress1)
            d["practice_info"].append({"practice_name": list(select_course)[0]["practice_name"],
                                       "practice_id": list(select_course)[0]["practice_id"],
                                       "progress": progress})
            # 对全量课程表中的第二行开始依此与第一行的practice_id进行比较，如果相同，在第一个progress添加相应字段；
            # 如果不同，在practice_info中添加新的practice_name并添加相应progress字段
            # k用于计数practice_info内list的项
            k = 0
            progress3 = []
            for i in range(1, len(list(select_course))):
                if list(select_course)[i]["practice_name"] == d["practice_info"][0 + k][
                    "practice_name"]:
                    progress2 = {}
                    progress2["practice_chapter_name"] = list(select_course)[i][
                        "practice_chapter_name"]
                    progress2["learn_status"] = list(select_course)[i]["learn_status"]
                    progress2["practice_chapter_id"] = list(select_course)[i]["practice_chapter_id"]
                    d["practice_info"][k]["progress"].append(progress2)
                else:
                    progress2 = {}
                    progress2["practice_chapter_name"] = list(select_course)[i][
                        "practice_chapter_name"]
                    progress2["learn_status"] = list(select_course)[i]["learn_status"]
                    progress2["practice_chapter_id"] = list(select_course)[i]["practice_chapter_id"]
                    progress3.append(progress2)
                    d["practice_info"].append(
                        {"practice_name": list(select_course)[i]["practice_name"],
                         "practice_id": list(select_course)[i]["practice_id"],
                         "progress": progress3})
                    k += 1
        print(d)
        return render(request, "course_display.html", d)