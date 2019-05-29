#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")

import jieba
import jieba.posseg
import jieba.analyse

'''
fpath = 'F:\\学习\\python\\python小说文本分析\\laojiumen.txt'
with open(fpath, 'r', encoding='utf-8') as f:
    sentence = f.read()
    for x, w in jieba.analyse.textrank(sentence, topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')):
        print('%s %s' % (x, w))
'''
jieba.add_word('Python')
sentence = "快乐学Python可以有效提升青少年的逻辑思维能力、引导启迪孩子对编程类学习的热爱，帮助孩子科学智能学习Python。同时快乐学Python为初学者准备了普适性强的实战项目，面向实际应用，助力职场发展。我们的目标是推出具有智能学习引导、优秀学习课程、上手简单的Python学习平台和课程，同时增加场景化工具集，解决青少年与初学者学习编程的问题。"
for x, w in jieba.analyse.textrank(sentence, topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')):
        print('%s %s' % (x, w))
print('-------------------------------------')
for x, w in jieba.analyse.textrank(sentence, topK=5, withWeight=True):
        print('%s %s' % (x, w))
print('-------------------------------------')
for x, w in jieba.analyse.extract_tags(sentence, topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')):
        print('%s %s' % (x, w))

print('-------------------------------------')
for x, w in jieba.analyse.extract_tags(sentence, topK=5, withWeight=True, allowPOS=()):
        print('%s %s' % (x, w))
