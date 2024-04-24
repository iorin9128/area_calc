from shapely import *
from math import *
import glob, sys, shutil, os
from  shapely import *

def load_cad_data_to_lines(area_name):
    lines = []
    path = f"./line_data/{area_name}.cad_data"
    with open(path,"r",encoding="Shift-JIS") as f:
        line = f.read().split("\n")
        for l in line:
            lines.append(LineString([(float(l.split()[0]),float(l.split()[1])),(float(l.split()[2]),float(l.split()[3]))]))
    return lines

class OutPutFile:
    def __init__(self,area_name):
        self.area_name = area_name
        self.path = f"./out_data/{area_name}.xlsx"
        self.lists_of_path = glob.glob(self.path)
        if not self.lists_of_path:
            shutil.copy(f"./out_data/様式_output.xlsx",f"./out_data/{self.area_name}.xlsx") 
        else:
            os.remove(self.path)
            shutil.copy(f"./out_data/様式_output.xlsx",f"./out_data/{self.area_name}.xlsx") 
            # sys.exit()

class Mesh:
    def __init__(self, step, index_x, index_y, base_polygon_for_cal):
        self.step = step
        self.index_x = index_x
        self.index_y = index_y
        self.base_polygon_for_cal = base_polygon_for_cal
    def intersection(self):
        mesh_polygon = Polygon([(self.index_x*self.step,self.index_y*self.step),
                                (self.index_x*self.step+self.step,self.index_y*self.step),
                                (self.index_x*self.step+self.step,self.index_y*self.step+self.step),
                                (self.index_x*self.step,self.index_y*self.step+self.step),
                                (self.index_x*self.step,self.index_y*self.step)])
        intersection = self.base_polygon_for_cal.intersection(mesh_polygon)
        return intersection
    
def lines_to_polygon(lines):
    if not polygonize(lines).is_empty:
        base_polygon_for_cal = polygonize(lines)
    else:
        print("not ring")
        sys.exit()
    return base_polygon_for_cal

def list_meshes_with_intersection(step,base_polygon_for_cal):
    meshes = []
    min_index_x = floor(base_polygon_for_cal.bounds[0]/step)
    min_index_y = floor(base_polygon_for_cal.bounds[1]/step)
    max_index_x = floor(base_polygon_for_cal.bounds[2]/step)
    max_index_y = floor(base_polygon_for_cal.bounds[3]/step)

    for x in range(min_index_x,max_index_x+1):
        #print(x)
        for y in range(min_index_y,max_index_y+1):
            #print(y)
            meshes.append(Mesh(step,x,y,base_polygon_for_cal))

    return meshes

def list_intersection_for_calc(list_meshes_with_intersection):
    list_intersection_for_calc = []
    for i in list_meshes_with_intersection:
        if not i.intersection().area == 0.0 and not i.intersection().area == 100.0:
            list_intersection_for_calc.append(i)
    return list_intersection_for_calc

def data_for_double_calculation(list_mesh_for_inter_calc):
    temp = []
    data_for_double_calculation = []
    for i in list_mesh_for_inter_calc:
        # print(i.intersection().geom_type)
        if i.intersection().geom_type == 'Polygon':
            temp.append([(i.index_x, i.index_y), list(i.intersection().boundary.coords)])
            # print(list(i.intersection().boundary.coords))
        elif i.intersection().geom_type == 'MultiPolygon':
            for k in list(i.intersection().geoms):
                temp.append([(i.index_x, i.index_y),list(k.boundary.coords)])
                # print(list(k.boundary.coords))
    for i in temp:
        i[1].pop()
        data_for_double_calculation.append(i)
    return data_for_double_calculation



