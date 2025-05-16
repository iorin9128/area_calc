from shapely.geometry import Polygon
from pathlib import Path
from utils_1 import *
import sys

def get_intersection(poly1_coords, poly2_coords):
    
    try:
        # ShapelyのPolygonオブジェクトを作成
        polygon1 = Polygon(poly1_coords)
        polygon2 = Polygon(poly2_coords)

        # ポリゴンが有効かチェック (オプションですが推奨)
        if not polygon1.is_valid:
            print("エラー: 1つ目のポリゴンが無効です。")
            # 必要に応じてエラー処理を追加
            # raise ValueError("1つ目のポリゴンが無効です。")
            return None
        if not polygon2.is_valid:
            print("エラー: 2つ目のポリゴンが無効です。")
            # raise ValueError("2つ目のポリゴンが無効です。")
            return None

        # 重なった部分を計算
        intersection_poly = polygon1.intersection(polygon2)

        return intersection_poly

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    
    log_file_path = "./test/autocad_log_8.log" 
    path_obj_file = Path(log_file_path)
    base_file_name = path_obj_file.stem

    # autocad のログファイルから x,yの座標を抽出する
    # args: 配列の配列
    parsers = parse_autocad_log_for_coordinates(log_file_path)
    if len(parsers) != 2:
        sys.exit(1)

    # x,yの座標配列の最初と最後が違うならば、最初を最後に追加する
    append_first_to_end_if_mismatched(parsers)

    # ポリゴンの配列をを作る
    # 例：<POLYGON ((48.237 36.228, 47.407 43.922, 56.411 43.803, ...>, 
    #   　<POLYGON ((22.94 12.662, 7.33 14.378, 5.406 24.502, ...>]
    polygon_list = []
    for l in parsers:
        polygon_list.append(create_polygon_from_xy_coords(l))
    
    intersection_polygon = get_intersection(polygon_list[0], polygon_list[1])
    
    coords = list(intersection_polygon.exterior.coords)

    for i in coords:
        print(f"{i[0]},{i[1]}")
    
    