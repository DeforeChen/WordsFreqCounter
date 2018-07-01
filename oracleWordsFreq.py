#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import punctuation
from zhon.hanzi import punctuation

from opencc import OpenCC
import re
import xlwt
import sys
import os
import string

reload(sys)
sys.setdefaultencoding('utf-8')

global wordCountDict, indexFileName
wordCountDict = {}  # 建立用于计算词频的空字典
indexFileName = {}  # 建立词频所属的文件的索引，和wordCountDict拥有相同的 key

# 对文本的每一行计算词频的函数
def processLine(line, fileName):
    # 用空格替换标点符号
    line = replaceZhonPunctuations(line)

    for word in line:
        if word in wordCountDict:
            wordCountDict[word] += 1
            if indexFileName[word].find(fileName) == -1:
                indexFileName[word] = indexFileName[word] + ',' + fileName
        else:
            wordCountDict[word] = 1
            indexFileName[word] = fileName

def replaceZhonPunctuations(line):
    # 去掉其中的中文标点符号
    noZhPuncLine = re.sub(ur"[%s]+" % punctuation, "", line.decode("utf-8"))
    # 去掉其中的英文标点符号
    noEnPuncLine = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),noZhPuncLine)
    # 去掉其中的英文或数字
    noEnLine = re.sub("[A-Za-z0-9]", "", noEnPuncLine)

    # 簡體轉化至繁體
    openCC = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
    finalLine = openCC.convert(noEnLine)
    # print(finalLine)

    return finalLine

# 处理单个文件
def singleFileCounter(filePath, filename):
    infile = open(filePath, 'r')

    # 建立用于计算词频的空字典
    for line in infile:
        processLine(line, filename)
    infile.close()


def main():
    words = []
    data = []

    # 遍历文件夹中所有的文档
    for fpathe, dirs, fs in os.walk('./文档/'):
        for filename in fs:
            if os.path.splitext(filename)[1] == '.txt':
                fileNameWithoutExp = os.path.splitext(filename)[0]
                filepath = os.path.join(fpathe, filename)
                print('当前文件名 ' + fileNameWithoutExp)
                singleFileCounter(filepath, fileNameWithoutExp)

    # 从字典中获取数据对
    pairs = list(wordCountDict.items())
    print(pairs)
    # 列表中的数据对交换位置,数据对排序
    items = [[x, y] for (y, x) in pairs]
    items.sort(reverse=True)

    count = len(wordCountDict)

    filepath = r'./test1.xls'

    book  = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)

    for i in range(len(items) - 1, len(items) - count - 1, -1):
        sheet.write(i, 0, str(items[i][0]))  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
        sheet.write(i, 1, str(items[i][1]))
        indexname = str(indexFileName[(items[i][1])])
        sheet.write(i, 2, indexname)

        data.append(items[i][0])
        words.append(items[i][1])

    book.save(filepath)

if __name__ == '__main__':
    main()