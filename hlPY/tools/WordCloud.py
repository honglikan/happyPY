# - * - coding: utf - 8 -*-

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from random import randint
from wordcloud import WordCloud, ImageColorGenerator

# 获取当前文件路径
d = path.dirname('.')

stopwords = {}
isCN = 1 #默认启用中文分词
back_coloring_path = "F:\python\danghui3.jpg" # 设置背景图片路径
text_path = 'F:\python\习近平：自主创新推进网络强国建设.txt' #设置要分析的文本路径
font_path = 'simkai.ttf' # 为matplotlib设置中文字体路径没
stopwords_path = 'F:\python\stopwords1893.txt' # 停用词词表
imgname1 = "F:\python\习近平：自主创新推进网络强国建设_1.png" # 保存的图片名字1(只按照背景图片形状)
imgname2 = "F:\python\习近平：自主创新推进网络强国建设_2.png"# 保存的图片名字2(颜色按照背景图片颜色布局生成)

my_words_list = ['习近平'] # 在结巴的词库中添加新词
back_coloring = imread(path.join(d, back_coloring_path))# 设置背景图片
def jiebaclearText(text):
    #定义一个空的列表，将去除的停用词的分词保存
    mywordList=[]
    #进行分词
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    #打开停用词表
    f_stop=open(stopwords_path,encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordList.append(myword)
    return ' '.join(mywordList)
# 设置词云属性
wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=500,  # 词云显示的最大词数
               mask=back_coloring,  # 设置背景图片
               max_font_size=150,  # 字体最大值
               random_state=30,
               width=1000, height=860, margin=2,# 设置图片默认的大小,保存的图片大小将会按照背景图片大小保存,margin为词语边缘距离
              )

# 添加自己的词库分词
def add_word(list):
    for items in list:
        jieba.add_word(items)

add_word(my_words_list)

text = open(path.join(d, text_path)).read()
text1=jiebaclearText(text)

# 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text1)
def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h = randint(0,50)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)
image_colors = ImageColorGenerator(back_coloring)

plt.figure()
# 以下代码显示图片
plt.imshow(wc.recolor(color_func=random_color_func),interpolation="bilinear")
plt.axis("off")
plt.savefig(imgname1,dpi=500)
plt.show()
# 绘制词云
image_colors = ImageColorGenerator(back_coloring)
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors),interpolation="bilinear")
plt.axis("off")
plt.savefig(imgname2,dpi=500)
plt.show()