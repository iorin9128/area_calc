from shapely import *
from utils_other import *
from utils_1 import *
import csv

# オートキャドのログファイルから X,Y座標を抽出する
line = u1.parse_autocad_log_for_coordinates("./data/汀線.log")

# X,Y座標からLineStringを作る
linestring = create_linestring_from_xy_coords(line[0])
# print(linestring)


# 距離の閾値を定義
# initial_point = Point(750,-500)
target_distance = 600.0

# point = find_point_within_distance_binary_search(linestring, initial_point, target_distance)
# print(point)

results = []
start_x = -800
end_x = 10500
step = 10
start_y = -2500

for x in range(start_x, end_x, step):
    start_point = Point(x, start_y)

    # 関数を実行して点を探索
    found_point = find_point_vertically_within_distance(linestring, start_point, target_distance)
    results.append(found_point)

resutls_1 = []
for i in results:
    if i is not None:
        temp = [i.x, i.y]
        resutls_1.append(temp)

filename = "output.csv"
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(resutls_1)
