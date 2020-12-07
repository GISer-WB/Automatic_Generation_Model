# coding:utf-8
# coding:utf-8
import xlwt
import xlrd
from py2neo import Graph, Node, Relationship

##连接neo4j数据库，输入地址、用户名、密码
graph = Graph('bolt://localhost:7687', username='neo4j', password='123456')

book = xlrd.open_workbook('./data.xlsx')
workSheetName = book.sheet_names() 
print("Excel文件包含的表单有："+str(workSheetName))


# 根据指定的表单名,一行一行获取指定表单中的所有数据，表单名为worksheetname
def GetAllSheetCellValue(worksheetname):
    bridgeStructure = book.sheet_by_name(worksheetname)
    AllsheetValue = []
    for i in range(bridgeStructure.nrows):
        for j in range(bridgeStructure.ncols):
            AllsheetValue.append(bridgeStructure.cell_value(i,j))
    # print("《"+str(worksheetname)+"》"+"数据获取成功，请指定变量接收")
    return AllsheetValue

# 根据指定的表单名，按列获取表单中的数据
def GetAllSheetValueByColum(worksheetname):
    bridgeStructure = book.sheet_by_name(worksheetname)#获取指定名称的表单
    col_nums = bridgeStructure.ncols #获取指定表单的有效列数
    # print(bridgeStructure)
    AllsheetValue = []
    for i in range(col_nums):
        AllsheetValue.append(bridgeStructure.col_values(i))
    # print(AllsheetValue)
    return AllsheetValue

# 创建一个指定节点类，名字，创建节点,其他属性有需要自定拓展这个方法
def CreateNode(className,lableName,name):
    test_node= Node(className,lable = lableName, name=name)
    graph.create(test_node)

# 指定表名，类名，名字，批量创建节点
def CreateNodes(worksheetname,lableName,ClassName):
    sheetvalue = GetAllSheetCellValue(worksheetname)
    nums = 0
    for i in range(len(sheetvalue)):
        CreateNode(ClassName,lableName,sheetvalue[i])
        nums+=1
    print("创建"+worksheetname+"节点成功，总计创建%s个"%(nums))

# 根据需要创建节点的表名个数(有几个表就传输参数是几)，批量创建节点，这个方法中默认构件类名就是图谱中的类名
# 参数说明 nums：在一个Excel文件中的需要创建节点的表单数
def CreateNodesBySheetNums(nums):
    for i in range(nums):
        CreateNodes(workSheetName[i], workSheetName[i],workSheetName[i])

#建立两个节点之间的关系
#参数说明 node1：节点1，node2：节点2，relationship：节点之间的关系
def CreateTwoNodeRelationship(node1,node2,relationship):
    relation = Relationship(node2, relationship, node1)
    graph.create(relation)

# 根据Excel文件中两个对象列表和一个关系列表，建立两个列表之间的子类（subclassof）关系
# 参数说明 worksheetname：指定的表单名,className1:第一个类的名称，className2：第二个类的名称
def subclassRelationship(worksheetname, className1,className2):
    list1 = GetAllSheetValueByColum(worksheetname)[0]
    list2 = GetAllSheetValueByColum(worksheetname)[2]
    relationship = GetAllSheetCellValue(worksheetname)[1]
    print(list1,relationship,list2)
    # 利用Python执行CQL语句
    

    num=0
    for i in range(len(list1)):
        num+=1
        graph.run("match(a:%s),(b:%s)  where a.name='%s' and b.name='%s'  CREATE (a)-[r:%s]->(b)"%(className1,className2,str(list2[i]),str(list1[i]),str(relationship)))
    print('创建%d个关系成功'%(num))

CreateNodesBySheetNums(4)

subclassRelationship(workSheetName[4],"Lithology_category","Rock_entity")
subclassRelationship(workSheetName[5],"Rock_entity","Rock_entity")
subclassRelationship(workSheetName[6],"Rock_entity","Thickness")
subclassRelationship(workSheetName[7],"Rock_entity","Dip_angle")
print("程序运行完成")

