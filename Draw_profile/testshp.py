# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import MultipleLocator
import heapq
import math 
from scipy.interpolate import make_interp_spline
from osgeo import ogr
import os
from ospybook.vectorplotter import VectorPlotter

class Drawprofile():
    def __init__(self):
        self.file_name1 = r'D:\code\bp\pmt\dem\ct\ele01.xlsx'
        self.file_name2 = r'D:\code\bp\pmt\data1.xlsx'

    def handle(self):
        self.elevation_points()
        self.endpoint()
        self.readdata()
        self.draw_profile()

    #读取高程点   
    def elevation_points(self):
        #file_name = r'D:\code\bp\pmt\dem\ct\ele.xlsx'
        df = pd.read_excel(self.file_name1, encoding="utf-8")
        df[["距离","高度"]].head()
        Obeject = np.array(df['距离'],dtype = float)
        Elevation = np.array(df['高度'],dtype = float)
        global xValue 
        global yValue 
        xValue = Obeject
        yValue = Elevation

    #检测剖面线起点
    def endpoint(self):
        
        min_number_x = heapq.nsmallest(1, xValue) 
        print(min_number_x)
        min_number_y = heapq.nsmallest(1, yValue)
        print(min_number_y)
        z=list(zip(min_number_x,min_number_y))
        print(z)
        self.p1 = (z[0])
        print (self.p1)
        self.max_number_x = heapq.nlargest(1,xValue)

    #读取倾角等数据
    def readdata(self):
        #file_name = 'D:\\code\\bp\\pmt\\data1.xlsx'
        df = pd.read_excel(self.file_name2, encoding="utf-8")
        df[["ID","属性","厚度/m","倾角/°", "倾向/°"]].head()
        global Attribute
        Attribute = np.array(df['属性'])
        global Tendency
        Tendency = np.array(df['倾向/°'])
        self.h=np.array(df['厚度/m'])
        self.Y=np.array(df['倾角/°'])
        print(self.h[:5])
        print(self.Y[:5])
        scale=2.5
        #将距离以列表形式存储
        self.X=[]
        for j in range(len(self.h)):
            r=list(np.atleast_1d(self.h[j])*scale)
            #print(r)
            self.X.extend(r)
        print(self.X)
        #将角度以列表形式存储
        self.R=[]
        for i in range(len(self.Y)):
            g = list(np.atleast_1d(math.radians(self.Y[i])))
            self.R.extend(g)
        print(self.R)     
    
    #绘制地质剖面图轮廓      
    def draw_profile(self):
        self.D=300
        self.c1=[]
        self.c2=[]
        line_s_x = self.p1[0]
        line_s_y = self.p1[1]
        self.coord = list(zip(xValue,yValue))
        global linexlist 
        linexlist = [self.p1[0]] 
        global lineylist 
        lineylist = [self.p1[1]]
        global linewxlist 
        linewxlist = [] 
        global linewylist 
        linewylist = []
        
        #拟合地形轮廓线
        m = np.array(xValue)
        n = np.array(yValue)
        f1 = np.polyfit(m, n, 30)
        print('f1 is :\n',f1)
        p0 = np.poly1d(f1)
        print('p0 is :\n',p0)
        
        extfile = r'D:\code\bp\pmt\dem\shape\1029expsideline04.shp'
        driver = ogr.GetDriverByName('ESRI Shapefile')
        if os.access(extfile,os.F_OK):
            driver.DeleteDataSource(extfile)
        newline = driver.CreateDataSource(extfile)
        linelyr = newline.CreateLayer('line',None,ogr.wkbLineString)
        fieldid = ogr.FieldDefn("id", ogr.OFTInteger)
        linelyr.CreateField(fieldid)
        fieldelevation = ogr.FieldDefn("name", ogr.OFTString)
        linelyr.CreateField(fieldelevation)
        
        #绘制每条界面线
        global path1
        for j in range(len(self.R)): 
            r1 = self.D*math.cos(self.R[j])
            r2 = self.D*math.sin(self.R[j])
            line_w_x=float(line_s_x+r1)
            line_w_y=float(line_s_y-r2)
            linewxlist.append(line_w_x)
            linewylist.append(line_w_y)
            plt.plot([line_s_x,line_w_x],[line_s_y,line_w_y],color='#000000') 
            path1 = ogr.Geometry(ogr.wkbLineString)
            path1.AddPoint(line_s_x,line_s_y)
            path1.AddPoint(line_w_x,line_w_y)
            linefeat = ogr.Feature(linelyr.GetLayerDefn())
            linefeat.SetField('id',j)
            linefeat.SetField('name','Line%d' %j)
            linefeat.SetGeometry(path1)
            linelyr.CreateFeature(linefeat)
            #斜率
            k = (line_w_y - line_s_y) / (line_w_x - line_s_x)
            #k = math.tan(self.R[j])
            #截距
            b = line_s_y - k * line_s_x
            for i in self.coord:
                self.point_x=i[0]
                self.point_y= p0(self.point_x)
                #带入公式得到距离dis
                dis = round(math.fabs(k * self.point_x - self.point_y + b) / math.pow(k * k + 1, 0.5),1)                 
                if ((dis == round(self.X[j],1)) and (self.point_x > line_s_x)):
                    print('self.point_x:',self.point_x) 
                    print('self.point_y:',self.point_y)
                    line_s_x=self.point_x
                    line_s_y=self.point_y
            print('line_s_x',line_s_x)
            linexlist.append(line_s_x)
            lineylist.append(line_s_y)
        
        s = len(linexlist)-1
        y_final = p0(linexlist[s])
        r1 = self.D*math.cos(self.R[len(self.R)-1])
        r2 = self.D*math.sin(self.R[len(self.R)-1])
        line_w_x1 = linexlist[s]+ r1
        line_w_y1 = y_final-r2 
        path2 = ogr.Geometry(ogr.wkbLineString)
        path2.AddPoint(linexlist[s],y_final)
        path2.AddPoint(line_w_x1,line_w_y1)
        linefeat = ogr.Feature(linelyr.GetLayerDefn())
        linefeat.SetField('id',(len(linexlist)-1))
        linefeat.SetField('name','Line%d' %(len(linexlist)-1))
        linefeat.SetGeometry(path2)
        linelyr.CreateFeature(linefeat)     
        
        #绘制地质剖面线
        x_ = np.array(linexlist)
        y_ = np.array(lineylist)
        x_smooth = np.linspace(x_.min(), x_.max(), 5000)
        y_smooth = make_interp_spline(x_, y_)(x_smooth)
        uplist = list(zip(x_smooth,y_smooth))
        path3 = ogr.Geometry(ogr.wkbLineString)
        for vertex1 in uplist:
            path3.AddPoint(*vertex1)  
        linefeat = ogr.Feature(linelyr.GetLayerDefn())
        linefeat.SetField('id',(len(linexlist)))
        linefeat.SetField('name','Line%d' %(len(linexlist)))
        linefeat.SetGeometry(path3)
        linelyr.CreateFeature(linefeat)
        
        #绘制连接线
        linewxlist.append(line_w_x1)
        linewylist.append(line_w_y1)
        downlist = list(zip(linewxlist,linewylist))
        path4 = ogr.Geometry(ogr.wkbLineString)
        for vertex2 in downlist:
            path4.AddPoint(*vertex2)  
        linefeat = ogr.Feature(linelyr.GetLayerDefn())
        linefeat.SetField('id',(len(linexlist)+1))
        linefeat.SetField('name','Line%d' %(len(linexlist)+1))
        linefeat.SetGeometry(path4)
        linelyr.CreateFeature(linefeat)