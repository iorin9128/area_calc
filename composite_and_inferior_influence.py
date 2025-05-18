from utils_1 import *
from shapely import *

# 影響範囲のポリゴンの x,y の座標の組を抽出する
# [[[2,3],[5,5],[0,0]],[[5,5],[2,4],[5,9]]] のような配列の配列
parsers = u1.parse_autocad_log_for_coordinates("./data/影響範囲800m.log")

# 影響の始まりの線分のログファイルから x,y 座標の組を抽出する
# [[[2,3],[5,5],[0,0]],[[5,5],[2,4],[5,9]]] のような配列
b_linestring = u1.parse_autocad_log_for_coordinates("./data/新用地幅杭.log")

# b_linestringの[0] を LineString にする
linestring = LineString(b_linestring[0])

# parsersの座標配列の最初と最後が違うならば、最初を最後に追加する
for l in parsers:
    append_first_to_end_if_mismatched(l)

# ポリゴンの組を作る
polygons_list = []
for l in parsers:
    polygons_list.append(create_polygon_from_xy_coords(l))
# print(polygons_list[0])


# ポリゴンのリストをGEOMETRYCOLLECTIONにする
collection = GeometryCollection(polygons_list)

# 計算範囲の座標を整数のタプルで出す
caluculatin_area = get_calculation_area(collection.bounds, 10)

# 計算エリアをGridAreaクラスに渡す
grid_aria = GridArea(caluculatin_area)

# 計算領域としての10*10のメッシュと、入力したポリゴンリストが重なっている領域だけを取り出す
# return : [(重複の仕方, 重複したポリゴン, mesh_cell)]
overlap_area = grid_aria.check_polygon_mesh_intersection(polygons_list[0])

# アウトプットを変更する
"""
    calc_composit_10
    
"""
flag = "calc_composit_10"

for i in overlap_area:
    print(i[2].index[0]*10,",",i[2].index[1]*10,",",i[2].calculate_composite_influence(linestring))
    # print(i[2].index[0]*10,",",i[2].index[1]*10,",",i[2].calculate_inferior_influence(linestring))
    # print(i[2].index[0],",",i[2].index[1],",",i[2].calculate_inferior_influence(linestring))
    



