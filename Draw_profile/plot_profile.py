# coding:utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import descartes
import numpy as np
from matplotlib.pyplot import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from matplotlib import colors,cm #自定义色彩
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

map_ = geopandas.read_file(r'D:\code\bp\pmt\dem\shape\topolygon\polygon.shp')
map_colors = ['teal','aqua','blue','gold','coral','moccasin','darkred','darkorange','green','khaki','darkmagenta','linen','darkviolet','lightskyblue','pink','mediumvioletred',
        'snow','darkgreen','yellow','tan','olive']
    
fig, ax = plt.subplots(1, figsize=(12,5))
my_cmap = colors.ListedColormap(map_colors,'indexed')

#out  = map_['_Lithology']
out  = map_['Rock_type']
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 10}
map_.plot(ax=ax, column = out, categorical=True, legend=True , 
            legend_kwds={'loc': 'lower right','ncol':1,'prop':font},           
            cmap=my_cmap)
            
x, y, arrow_length = 0.03, 0.95, 0.1
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=4, headwidth=7),
            ha='center', va='center', fontsize=10,
            xycoords=ax.transAxes)
            
scalebar = ScaleBar(dx=1*10**-3,units='km',length_fraction=0.1,
                    font_properties={'family': 'Times New Roman', 'weight': 'normal', 'size': 12},
                    location=8,sep=1,frameon=False)



ax.add_artist(scalebar)

plt.xlim(-50,5500)
plt.ylim(3500,5500)
plt.xlabel('Distance/m',fontdict={'family' : 'Times New Roman', 'size'   : 10})
plt.ylabel('Elevation/m',fontdict={'family' : 'Times New Roman', 'size'   : 10})  
#plt.title('Automatic reconstruction of the geological profile map',fontdict={'family' : 'Times New Roman', 'size'   : 16})
plt.title('Lithology classification analysis',fontdict={'family' : 'Times New Roman', 'size' : 16})
plt.savefig('./classification.png',dpi=400)
#plt.savefig('./lithology.png',dpi=400)
plt.show()
