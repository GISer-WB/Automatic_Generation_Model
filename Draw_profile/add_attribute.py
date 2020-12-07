#利用python2.7运行
# coding:utf-8
import arcpy
import xlrd

filename = 'D:\\code\\bp\\pmt\\dem\\shape\\topolygon'
arcpy.env.workspace = filename
shppath = 'D:\\code\\bp\\pmt\\dem\\shape\\topolygon\\polygon.shp'

worksheet = xlrd.open_workbook(r'D:\code\bp\pmt\data1.xlsx')
sheet= worksheet.sheet_by_name('Sheet1')
cols = sheet.ncols # 获取列数，尽管没用到
rows = sheet.nrows # 获取行数
all_content = []
for i in range(1,rows) :
    cell = sheet.cell_value(i, 2) # 取第二列数据
    #cell = str(cell) # 转换
    all_content.append(cell)

cursor = arcpy.UpdateCursor(shppath)
i = 0
for my_row in cursor:
    my_value = my_row.getValue('Width')
    my_row.setValue('Width', all_content[i])
    cursor.updateRow(my_row)
    i += 1
print("finish!")