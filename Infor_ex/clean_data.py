import re
from pyhanlp import *
import pandas as pd

def readFile(path):
    '''
    提取岩层描述信息
    '''
    str_doc = ""
    pattern = re.compile(r'([\u4e00-\u9fa5, ]{1})\s+([\u4e00-\u9fa5, ]{1})')
    #去除空行，删除换行符
    r1 = "^\s*\n"
    #查找各岩层描述
    r2 = r"\d\d\. [\u4e00-\u9fa5].*|\d\. [\u4e00-\u9fa5].*"
    #去除岩层中不存在的厚度，如 1635.4m
    r3 = r"[\u4e00-\u9fa5] [1-9] [1-9][1-9]?[0-9](\.[0-9]+)\ m"
    with open(path,'r',encoding='utf-8') as f:
        str_doc = f.read()
    str_doc=re.sub(r1, ' ', str_doc)
    
    str2 = pattern.sub(r'\1\2',str_doc)
    str2 = str2.strip()+"\n"
    str3 = re.sub(r3,' ',str2)
    str3 = re.findall(r2, str3)
    
    str_out_list = []
    for i in str3:
        str_out = re.sub(r"\d\d\. |\d\. ",'',i)
        str_out_list.append(str_out)   
    
    '''
    提取各岩层厚度
    '''
    r4 = r"＞\d\d\d\.\d m|＞\d\d\.\d m|～\d\.\d m"
    r5 = r"\d\.\d m|\d\d\.\d m|\d\d\d\.\d m"
    str4 = re.sub(r4, ' ',str_doc)
    
    str4 = re.sub(r3, ' ',str4)
    str4 = re.findall(r5,str4)
    print (str4)
    '''
    48.厚度提取
    '''
    r6 = r"＞\d\d\.\d m"
    str5 = re.findall(r6,str_doc)
    r7 = r"＞"
    str6 = re.sub(r7,'',str5[0])
    str4.insert(0,str6)
   
    data ={
            'Description':str_out_list[::-1],
            'Width':str4[::-1]
          }
    # list转dataframe
    df = pd.DataFrame(data)
    
    # 保存到本地excel
    df.to_excel(r"D:\code\bp\pmt\dem\infor_extract\outfiles\outdes.xlsx", index=True)
    

if __name__ == '__main__': 
    path= r'D:\code\bp\pmt\dem\infor_extract\outfiles\outtext.txt'
    readFile(path)