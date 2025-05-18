import re
import shapely as sp
import math
import sys
from typing import List, Tuple, Union

def append_first_to_end_if_mismatched(lists_of_list):
    # テストケース作成済
    """配列の最初と最後が違うならば、最初を最後に追加する
    """
    for lists in lists_of_list:
        if lists[0] != lists[-1]:
            lists.append(lists[0])

def parse_autocad_log_for_coordinates(file_path) -> List[List[tuple]]:
    # テストケース作成済
    """オートキャドのログファイル(生ファイル)から 単純にX=... , Y=... から座標を抽出する

    Args:
        file_path:ファイルのパス

    Returns:
        [[[2,3],[5,5],[0,0]],[[5,5],[2,4],[5,9]]] のような配列の配列
    """

    number_strings = []
    with open(file_path, "r", encoding = 'utf-8') as f:
        for i in f:
            match = re.search(r"(.*)画層:", i)
            if match:
                if match.group(1).strip() == "LWPOLYLINE":
                    continue
                else:
                    print("ポリライン以外が存在しています")
                    sys.exit(1)
            number_strings.append(i.rstrip("\n"))

    group = []
    number_groups = []

    for i, number_string in enumerate(number_strings):
        match = re.search(r"X=(.*)\s+Y=(.*)\s+Z=", number_string)

        if match:
            x = float(match.group(1))
            y = float(match.group(2))
            group.append([x,y])

            # 次の数字がないか、次の要素が数字でない場合にグループを区切る
            if i + 1 == len(number_strings) or not re.search(r"X=(.*)\s+Y=(.*)\s+Z=", number_strings[i+1]):
                number_groups.append(group)
                group = []

    return number_groups

def remove_last_if_matches_first(lists):
    # テストケース作成済
    """配列の最初と最後が同じならば、最後を破壊的に削除する
    
        Args:
            配列
    
    """
    
    if len(lists) >= 2 and lists[0] == lists[-1]:
        lists.pop()
    


def create_linestring_from_xy_coords(xy):
    # テストケース作成済
    """[[x1,y1],[x2,y2], ....] からshapelyのLineStringを作る
        Args: 配列 [[x1,y1],[x2,y2], ....]

        return: shapelyオブジェクトの LineString
    """
    validated_coords = []
    for point in xy:
        validated_coords.append(tuple(point))
    return sp.LineString(validated_coords)
    


def create_polygon_from_xy_coords(xy):
    # テストケース作成済
    """ [[x1,y1],[x2,y2], ...., [x1,y1]] からshapelyのポリゴンを作る

    Args: [[x1,y1],[x2,y2], ...., [x1,y1]]
    return ポリゴン
    """
    b = []
    a = [list(p) for p in zip(xy, xy[1:])]
    for i in a:
        b.append(sp.LineString(i))
    geomss = sp.polygonize(b)
    return list(geomss.geoms)[0]

def merge_geometry_collections(collections):
    """配列に入った複数のGEOMETRYCOLLECTIONを統合して1つにする
    """
    all_geometries = list()
    for i in collections:
        all_geometries = all_geometries + list(i.geoms)

    merged_gc = sp.GeometryCollection(all_geometries)
    return merged_gc

def get_calculation_area(bounds_tuples, step):
    # テストケース作成済
    """タプル(x_min,y_min,x_max,y_max)から、stepでのメッシュでの計算範囲をタプルで出す。

        Args:
            (x_min,y_min,x_max,y_max)
        Returns:
            タプル
            minをstepで切り捨て。maxをstepで切り上げ。
    """
    # print(bounds_tuples)
    result_float_x_min = math.floor(bounds_tuples[0] / step) * step
    result_float_y_min = math.floor(bounds_tuples[1] / step) * step
    result_float_x_max = math.ceil(bounds_tuples[2] / step) * step
    result_float_y_max = math.ceil(bounds_tuples[3] / step) * step
    result_int_x_min = int(result_float_x_min)
    result_int_y_min = int(result_float_y_min)
    result_int_x_max = int(result_float_x_max)
    result_int_y_max = int(result_float_y_max)

    return (result_int_x_min, result_int_y_min, result_int_x_max, result_int_y_max)

def create_10m_mesh_polygons(caluculatin_area):
    # テストケース作成済
    """
    指定された領域内に10m x 10mのメッシュポリゴンを作成します。

    Args:
        caluculatin_area: タプル。(x_min, y_min, x_max, y_max)。

    Returns:
        list[Polygon]: 生成されたPolygonオブジェクトのリスト。
    """

    polygons = []
    mesh_size = 10  # メッシュサイズは10m
    x_min = caluculatin_area[0]
    y_min = caluculatin_area[1]
    x_max = caluculatin_area[2]
    y_max = caluculatin_area[3]

    # range関数はstop値を含まないため、x_max, y_maxまでループが回るようにする
    # x座標でループ
    for x in range(x_min, x_max, mesh_size):
        # y座標でループ
        for y in range(y_min, y_max, mesh_size):
            # ポリゴンの頂点を定義 (左下から時計回りまたは反時計回り)
            bottom_left = (x, y)
            bottom_right = (x + mesh_size, y)
            top_right = (x + mesh_size, y + mesh_size)
            top_left = (x, y + mesh_size)

            # Shapely Polygonオブジェクトを作成
            # 頂点のリスト (またはタプル) を渡す
            polygon = sp.Polygon([bottom_left, bottom_right, top_right, top_left])
            polygons.append(polygon)

    return polygons

class MeshCell:
    """それぞれのメッシュを表すクラス
    """
    def __init__(self, each_polygon):
        self.polygon = each_polygon

        # メッシュの重心をPointで返す
        self.center_point = each_polygon.centroid

        """メッシュ位置としてインデックスを定義する
            return (index_x,index_y)
        """
        # テストケース作成済
        self.index = (int(each_polygon.bounds[0] / 10),int(each_polygon.bounds[1] / 10))
        
    
    def calculate_composite_influence(self, linestring):
        # テストケース作成済
        self.distance = round(self.center_point.distance(linestring), 3)
        if self.distance < 0:
            self.influence_ratio = 1.0
        elif self.distance <= 500:
            self.influence_ratio = 1.0
        elif self.distance <=800:
            self.influence_ratio = (800.0 - self.distance) / (800.0 - 500.0)
        else:
            self.influence_ratio = 0.0
        return round(self.influence_ratio, 4)

    def calculate_inferior_influence(self, linestring):
        # テストケース作成済
        self.distance = round(self.center_point.distance(linestring), 3)
        if self.distance < 0:
            self.influence_ratio = 0.0
        elif self.distance <= 500:
            self.influence_ratio = 0.0
        elif self.distance <=800:
            self.influence_ratio = self.distance / 300.0 - 5.0/3.0
        else:
            self.influence_ratio = 1.0
        return round(self.influence_ratio, 4)

    def check_polygon_mesh_intersection(self, input_polygon):
        """ mesh_cell の self.polygonと、入力したポリゴンの重複の処理を行う
            return : [(重複の仕方, 重複したポリゴン, mesh_cell)]
        """
        intersection_geom = self.polygon.intersection(input_polygon)
        if intersection_geom.geom_type == "Polygon":
            if intersection_geom.area == 100.0:
                return ("all_overlap", intersection_geom, self)
            elif intersection_geom.area > 0.0:
                return ("partial_overlap", intersection_geom, self)
            elif intersection_geom.area == 0.0:
                return ("None", intersection_geom, self)
        elif intersection_geom.geom_type == "MultiPolygon":
            # print("重複したポリゴンはMultiPolygonで、",intersection_geom)
            return("multipolygon", intersection_geom, self)
        else:
            print(intersection_geom.geom_type)
            sys.exit(1)

class GridArea:
    """メッシュ全体を表すクラス。
    """
    def __init__(self, caluculatin_area):

        # 渡した計算領域から個々のメッシュを作って配列にする
        self.polygons = create_10m_mesh_polygons(caluculatin_area)

        # 各々のメッシュを、クラス「MeshCell」のインスタンスに入れる。
        self.mesh_list = []
        for i in self.polygons:
            self.mesh_list.append(MeshCell(i))

def check_MeshList_polygon_overlap(mesh_list, polygon_list):
    # 10m×10mメッシュと与えたポリゴンの重なり方を判定する
    # (重なり方、重複したポリゴン、meshインスタンス)
    check_mesh = []
    for mesh in mesh_list:
        mesh: MeshCell = mesh
        for polygon in polygon_list:
            check_mesh.append(mesh.check_polygon_mesh_intersection(polygon))
    return check_mesh