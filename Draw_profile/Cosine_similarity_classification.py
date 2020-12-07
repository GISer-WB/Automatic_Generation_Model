# coding:utf-8
import pandas as pd
import numpy as np
import re
import jieba


def rock_property(path):
    result = []
    out_list = []
    out_list1 = []
    df = pd.read_excel(path, encoding="utf-8",usecols=[1],names=None)
    att = df.values.tolist()

    for s_li in att:
        result.append(s_li[0])

    r1 = r'色(.*?)岩'
    for j in range(len(result)):
        out = re.findall(r1,result[j])
        if len(out)> 1:
            out_l = str(j+1)+'_' + out[0]+'岩'+'、'+out[1]+'岩'
            out1 = out[0]+'岩'+'、'+out[1]+'岩'
        else:
            out_l = str(j+1) + '_' + out[0] +'岩'
            out1 = out[0]+'岩'
        out_list.append(out_l)
        out_list1.append(out1)
    return out_list,out_list1

def get_word_vector(s1,s2):
    """
    :param s1: 句子1
    :param s2: 句子2
    :return: 返回句子的余弦相似度
    """
    # 分词
    cut1 = jieba.cut(s1)
    cut2 = jieba.cut(s2)
    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    # 输出向量
    #print(word_vector1)
    #print(word_vector2)
    return word_vector1, word_vector2

def cos_dist(vec1,vec2):
    """
    :param vec1: 向量1
    :param vec2: 向量2
    :return: 返回两个向量的余弦相似度
    """
    dist1=float(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    return dist1

def filter_html(html):
    """
    :param html: html
    :return: 返回去掉html的纯净文本
    """
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',html).strip()
    return dd


if __name__ == '__main__':
    file_path = r'D:\code\bp\pmt\data1.xlsx'
    out,out1 = rock_property(file_path)
    print (out,out1)
    
    lithology_list = ['泥岩','泥板岩','石英砂岩','石英粉砂岩','灰岩']
    for k in range(len(lithology_list)):
        for l in range(len(out1)):
            s1 = lithology_list[k]
            s2 = out1[l]
            if '、' in s2:
                s2_out = s2.split('、')
                s3 = s2_out[0]
            else:
                s3 = s2
            vec1,vec2=get_word_vector(s1,s3)
            dist1=round(cos_dist(vec1,vec2),3)
            if dist1 >= 0.5:
                print (s1 , s2, l, dist1)
            
