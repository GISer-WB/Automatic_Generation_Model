#利用python2.7运行
import arcpy
arcpy.env.workspace = "D:/code/bp/pmt/dem/shape"
arcpy.FeatureToPolygon_management(["profile.shp"],"D:\\code\\bp\\pmt\\dem\\shape\\topolygon\\polygon","", "NO_ATTRIBUTES")