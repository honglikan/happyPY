#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")

import jieba
import jieba.posseg
import jieba.analyse


fpath = 'F:\\学习\\python\\python小说文本分析\\laojiumen.txt'
with open(fpath, 'r', encoding='utf-8') as f:
    sentence = f.read()
    for x, w in jieba.analyse.textrank(sentence, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')):
        print('%s %s' % (x, w))