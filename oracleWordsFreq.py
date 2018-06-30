#!/usr/bin/env python
# -*- coding: utf-8 -*-


from string import punctuation
from zhon.hanzi import punctuation
import re
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 对文本的每一行计算词频的函数
def processLine(line, wordCounts):
    # 用空格替换标点符号
    line = replaceZhonPunctuations(line)
    # print(line)
    for word in line:
        # print(word)
        if word in wordCounts:
            wordCounts[word] += 1
        else:
            wordCounts[word] = 1

def replaceZhonPunctuations(line):
    # 去掉其中的中文标点符号
    noZhPuncLine = re.sub(ur"[%s]+" % punctuation, "", line.decode("utf-8"))
    noEnPuncLine = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),noZhPuncLine)
    return noEnPuncLine

def main():
    infile = open("/Users/Chen/Documents/Python/DivideWords/桃花源记.txt", 'r')

    words = []
    data = []

    # 建立用于计算词频的空字典
    wordCounts = {}
    for line in infile:
        processLine(line, wordCounts)  # 这里line.lower()的作用是将大写替换成小写，方便统计词频
    # 从字典中获取数据对
    pairs = list(wordCounts.items())
    # 列表中的数据对交换位置,数据对排序
    items = [[x, y] for (y, x) in pairs]
    items.sort(reverse=True)

    count = len(wordCounts)

    filepath = r'./test1.xls'


    book  = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)

    for i in range(len(items) - 1, len(items) - count - 1, -1):
        print(items[i][1] + "\t" + str(items[i][0]))
        sheet.write(i, 0, str(items[i][0]).decode('utf-8'))  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
        sheet.write(i, 1, str(items[i][1]).decode('utf-8'))
        data.append(items[i][0])
        words.append(items[i][1])

    book.save(filepath)
    infile.close()

if __name__ == '__main__':
    main()