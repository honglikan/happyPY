#-*- coding:utf8 -*-
import os, sys, subprocess, tempfile, time

# 创建临时文件夹,返回临时文件夹路径
TempFile = tempfile.mkdtemp(prefix='python_')
# 文件名
FileNum = int(time.time() * 1000)
# python编译器位置
EXEC = sys.executable

class TimeoutException(Exception): pass

# 获取python版本
def get_version():
    v = sys.version_info
    version = "python %s.%s" % (v.major, v.minor)
    return version


# 获得py文件名
def get_pyname():
    global FileNum
    return 'test_%d' % FileNum


# 接收代码写入文件
def write_file(pyname, code):
    fpath = os.path.join(TempFile, '%s.py' % pyname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('file path: %s' % fpath)
    return fpath


# 编码
def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')

        # 主执行函数


def main(code):
    r = dict()
    r["version"] = get_version()
    pyname = get_pyname()
    fpath = write_file(pyname, code)
    try:
        # subprocess.check_output 是 父进程等待子进程完成，返回子进程向标准输出的输出结果
        # stderr是标准输出的类型
        outdata = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=120))
    except subprocess.CalledProcessError as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["code"] = 'Error'
        r["output"] = decode(e.output)
        return r
    except subprocess.TimeoutExpired as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["code"] = 'Error'
        r["output"] = '您的程序已超时'
        return r
    else:
        # 成功返回的数据
        r['output'] = outdata
        r["code"] = "Success"
        return r
    finally:
        # 删除文件(其实不用删除临时文件会自动删除)
        try:
            os.remove(fpath)
        except Exception as e:
            exit(1)


def correct(file):
    r = dict()
    r["version"] = get_version()
    pyname = get_pyname()
    try:
        print(EXEC)
        # subprocess.check_output 是 父进程等待子进程完成，返回子进程向标准输出的输出结果
        # stderr是标准输出的类型
        outdata = decode(subprocess.check_output([EXEC, file], stderr=subprocess.STDOUT, timeout=120))
    except subprocess.CalledProcessError as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["code"] = 'Error'
        r["output"] = decode(e.output)
        return r
    except subprocess.TimeoutExpired as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["code"] = 'Error'
        r["output"] = '您的程序已超时'
        return r
    else:
        # 成功返回的数据
        r['output'] = outdata
        r["code"] = "Success"
        return r






if __name__ == '__main__':
  #code = "import math           math.sqrt(16)"

  code = "from __future__ import unicode_literals import matplotlib.pyplot as plt   from PIL import Image import numpy as np import jieba from wordcloud import WordCloud, ImageColorGenerator text = open('F:\\学习\\python\\python小说文本分析\\laojiumen.txt', 'r', encoding='utf-8').read() cut_text = jieba.cut(text, cut_all=False) result = '/'.join(cut_text) image = Image.open('C:\\Users\\liuxi\\Pictures\\logo2.PNG') graph = np.array(image) wc = WordCloud(font_path='simkai.ttf', background_color='white', max_font_size=50,mask=graph) wc.generate(result) image_color = ImageColorGenerator(graph)  wc.recolor(color_func=image_color) plt.figure('词云图') plt.imshow(wc)  plt.axis('off')  plt.show()"
  result=main(code)
  file = 'E:\\python\\happyPY\\hlPY\\results\\practice\\test.txt'
  result1=correct(file)
  print(result)
  print(result1)
  if result == result1:
      print('yes')
  else:
      print('no')


