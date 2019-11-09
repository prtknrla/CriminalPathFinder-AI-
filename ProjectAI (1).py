#!/usr/bin/env python
# coding: utf-8

# In[2]:


import geopandas as gpd
from statistics import median
from shapely.geometry import Polygon
import shapefile
import math
import numpy as np
sf=shapefile.Reader('crime_dt.shp')
points = gpd.read_file('crime_dt.shp')
print(sf)
print(points)


# In[4]:


#xmin,ymin,xmax,ymax =  points.total_bounds
xmin=-73.59
ymin=45.49
xmax=-73.55
ymax=45.53
gridsize=.002
cols=np.arange(xmin,xmax,gridsize)
rows=np.arange(ymin,ymax,gridsize)
print(len(cols))
print(len(rows))


# In[5]:


createPolygons=[]
cent=[]
for i in rows:
    y1=i
    y2=y1+gridsize
    for j in cols:
        x1=j
        x2=x1+gridsize
        createPolygons.append(Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]))
        cent.append(Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]).centroid)


# In[6]:


crs = {'init' :'epsg:4326'}
grid=gpd.GeoDataFrame({'geometry':createPolygons},crs=crs)


# In[7]:


grid.to_file("grid.shp")
poly=gpd.read_file("grid.shp")
print(len(poly))


# In[13]:


from geopandas.tools import sjoin
pointInPolys = sjoin(points, poly, how='left')
print(pointInPolys)


# In[14]:


finalPrint=[]
for index,row in poly.iterrows():
    attachPoints =  pointInPolys[pointInPolys.FID ==index ]
    finalPrint.append(len(attachPoints))

print(sum(finalPrint))
sortColor=finalPrint
print(np.median(sortColor))
print(np.mean(finalPrint))
print(np.std(finalPrint))


# In[28]:


print(len(finalPrint))
color=[]
FID=[]
countID=0
th=32
for x in finalPrint:
    if x>=75:
        FID.append(countID)
        countID=countID+1
        color.append('yellow')
    else:
        FID.append(countID)
        countID=countID+1
        color.append('purple')
print(len(color))
print(len(createPolygons))
print(len(FID))
print(len(rows))
print(len(cols))
print("Hello")
i=0
final_list = []
while i<len(cols)+1:
    j=0
    while j<len(rows)+1:
        temp = dict()
        temp['id'] = i*(len(rows) +1)+ j
        temp['x'] = j
        temp['y'] = i
        temp['is_visited'] = 0
        temp['h'] = len(rows)-temp['x'] if len(rows)-temp['x'] > len(cols)-temp['y'] else len(cols)-temp['y']
        temp['g'] = -1
         
        temp_color = []
        if temp['x']-1>=0 and temp['y']-1>=0:
            val = i
            if i != 0:
                val = val-1
            big = (val * 2)*len(rows) + len(rows)-1   
            temp_color.append(color[big -((temp['x']-1) + (temp['y']-1)*len(rows))])
        else:
            temp_color.append("red")
        
        if temp['x']-1>=0 and temp['y']+1<=len(cols):
            val = i
            if i != 0:
                val = val-1
            big = (val * 2)*len(rows) + len(rows)-1   
            temp_color.append(color[big -((temp['x']-1) + (temp['y'])*len(rows))])
        else:
            temp_color.append("red")
            
        if temp['x']+1<=len(rows) and temp['y']+1<=len(cols):
            val = i
            if i != 0:
                val = val-1
            big = (val * 2)*len(rows) + len(rows)-1    
            temp_color.append(color[big -((temp['x']) + (temp['y'])*len(rows))])
        else:
            temp_color.append("red")
            
        if temp['x']+1<=len(rows) and temp['y']-1>=0:
            val = i
            if i != 0:
                val = val-1
            big = (val * 2)*len(rows) + len(rows)-1   
            temp_color.append(color[big -((temp['x']) + (temp['y']-1)*len(rows))])
        else:
            temp_color.append("red")
        
        
        
        
        temp['color'] = temp_color
        temp['parent'] = -1
        final_list.append(temp)
        j=j+1
        
    i = i +1

print(len(final_list))
m = 0
while m<len(final_list):
    print(final_list[m])
    m=m+1

current_node = 0
final_list[current_node]['is_visited'] = 1;
final_list[current_node]['parent'] = -1;
final_list[current_node]['g'] = 0;
current_node = 22
final_list[current_node]['parent'] = 0;
while current_node != 461:
    x = final_list[current_node]['x']
    y = final_list[current_node]['y']
    colr = final_list[current_node]['color']
    min_f = 100000
    next_node = -1
    if (x-1>=0 and y-1>=0) and (final_list[((x-1)*(len(rows) +1))+ y-1]['is_visited'] == 0) and (colr[0] == 'purple' and (colr[1] == 'purple' or colr[3] == 'purple')):
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + 1.5
        if min_f>temp:
            print("H1")
            min_f = temp
            next_node = ((x-1)*(len(rows) +1))+ y-1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1.5
    if (x-1>=0) and (final_list[current_node-1]['is_visited'] == 0) and ((colr[0] == 'purple' and colr[1] == 'purple') or (colr[1] == 'purple' or colr[0] == 'yellow') or (colr[1] == 'yellow' or colr[0] == 'purple') ):
        val1 = 1.3    
        if (colr[0] == 'purple' and colr[1] == 'purple'):
            val1 = 1
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + val1
        if min_f>temp:
            print("H2")
            min_f = temp
            next_node = current_node-1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + val1
    if (x-1>=0 and y+1<=len(cols)) and (final_list[((y+1)*(len(rows)+1)) + x-1]['is_visited'] == 0) and (colr[1] == 'purple' and (colr[0] == 'purple' or colr[2] == 'purple')):
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + 1.5
        if min_f>temp:
            print("H3")
            min_f = temp
            next_node = ((y+1)*(len(rows)+1)) + x-1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1.5
    if (y+1<=len(cols)) and (final_list[((y+1)*(len(rows)+1)) + x]['is_visited'] == 0) and ((colr[1] == 'purple' and colr[2] == 'purple') or (colr[1] == 'purple' or colr[2] == 'yellow') or (colr[1] == 'yellow' or colr[2] == 'purple') ):
        val1 = 1.3    
        if (colr[1] == 'purple' and colr[2] == 'purple'):
            val1 = 1
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + val1
        if min_f>temp:
            print("H4")
            min_f = temp
            next_node = ((y+1)*(len(rows)+1)) + x
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + val1
    if (y+1<=len(cols) and x+1<=len(rows)) and (final_list[((y+1)*(len(rows)+1)) + x+1]['is_visited'] == 0) and (colr[2] == 'purple' and (colr[1] == 'purple' or colr[3] == 'purple')):
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + 1.5
        if min_f>temp:
            print("H5")
            min_f = temp
            next_node = ((y+1)*(len(rows)+1)) + x+1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1.5
    if (x+1<=len(rows)) and (final_list[current_node+1]['is_visited'] == 0) and ((colr[2] == 'purple' and colr[3] == 'purple') or (colr[2] == 'purple' or colr[3] == 'yellow') or (colr[2] == 'yellow' or colr[3] == 'purple') ):
        val1 = 1.3    
        if (colr[2] == 'purple' and colr[3] == 'purple'):
            val1 = 1
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + val1
        if min_f>temp:
            print("H6")
            min_f = temp
            next_node = current_node+1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + val1
    if (x+1<=len(rows) and y-1>=0) and (final_list[((y-1)*(len(rows)+1)) + x+1]['is_visited'] == 0) and (colr[3] == 'purple' and (colr[2] == 'purple' or colr[0] == 'purple')):
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + 1.5
        if min_f>temp:
            print("H7")
            min_f = temp
            next_node = ((y-1)*(len(rows)+1)) + x+1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1.5
    if (y-1>=0) and (final_list[((y-1)*(len(rows)+1)) + x]['is_visited'] == 0) and ((colr[3] == 'purple' and colr[0] == 'purple') or (colr[0] == 'purple' or colr[3] == 'yellow') or (colr[0] == 'yellow' or colr[3] == 'purple') ):
        val1 = 1.3    
        if (colr[3] == 'purple' and colr[0] == 'purple'):
            val1 = 1
        temp = final_list[current_node]['h'] + final_list[final_list[current_node]['parent']]['g'] + val1
        if min_f>temp:
            print("H8")
            min_f = temp
            next_node = ((y-1)*(len(rows)+1)) + x
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + val1
    
    if (y == len(cols) and x == 0):
        temp = final_list[current_node]['h'] + 1.5
        if min_f>temp and final_list[((y-1)*(len(rows) +1))+ x+1]['is_visited'] != 1:
            print("H9")
            min_f = temp
            next_node = ((y-1)*(len(rows) +1))+ x+1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1.5
        temp = final_list[current_node]['h'] + 1
        if min_f>temp and final_list[current_node+1]['is_visited'] != 1:
            print("H10")
            min_f = temp
            next_node = current_node+1
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1
        elif min_f>temp and final_list[(y-1)*(len(rows) +1)]['is_visited'] != 1:
            print("H11")
            min_f = temp
            next_node = (y-1)*(len(rows) +1)
            final_list[current_node]['g'] =  final_list[final_list[current_node]['parent']]['g'] + 1
    
    print("HAHAH")
    print(current_node)
    print(next_node)
    print(min_f)
    print("\n")
    if min_f != 100000:        
        final_list[next_node]['parent'] = current_node
        final_list[current_node]['is_visited'] = 1
        current_node = next_node
    else:
        print("No path found")
        break

    


# In[46]:


gridFinal=gpd.GeoDataFrame({'geometry':createPolygons,'NPoints':finalPrint,'colors':color,'FID':FID},crs=crs)
gridFinal.head()


# In[41]:


gridFinal.plot(column='colors',cmap='viridis')


# In[ ]:


gridFinal.


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




