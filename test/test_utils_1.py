import utils_1 as u1
from study import *
import pytest
from main_2 import *
import shapely as sp
from typing import List, Tuple

def test_parse_autocad_log_for_coordinates():
    """オートキャドのテストログをインポートして、ポリゴンごとの座標データとなっているか
        [[[2,3],[5,5],[0,0]],[[5,5],[2,4],[5,9]]] のような配列となっているか
    """
    path = "./test/autocad_log_1.log"
    a = u1.parse_autocad_log_for_coordinates(path)
    
    assert a[0][0] == [6138.166252, 640.702455] 
    assert a[1][3] == [4240.517868, 760.705001]

    # 一番最初を一番後ろに回しているか
    # assert a[1][4] == [4660.882982, 1192.714106]

def test__parse_autocad_log_for_coordinates():
    """LWPOLYLINE 以外があったら終了するか
    """
    path = "./test/autocad_log_4.log"
    with pytest.raises(SystemExit) as excinfo:
        u1.parse_autocad_log_for_coordinates(path)
    assert excinfo.value.code == 1

def test_remove_last_if_matches_first():
    """配列の最初と最後が同じならば、最後を破壊的に削除する
    """
    a = [[1.11,2.23],[3.11,4.55],[3.14,5.55],[1.11,2.23]]
    u1.remove_last_if_matches_first(a)
    if a == [[1.11,2.23],[3.11,4.55],[3.14,5.55]]:
        assert True
    else:
        assert False

def test_append_first_to_end_if_mismatched():
    """配列の最初と最後が違うならば、最初を最後に追加する
    """
    a: List[List[Tuple[float, float]]] = [[[1.11,2.23],[3.11,4.55],[3.14,5.55]],[[1.11,2.23],[3.11,4.55],[3.14,5.55],[1.11,2.23]]]
    u1.append_first_to_end_if_mismatched(a)
    if a == [[[1.11,2.23],[3.11,4.55],[3.14,5.55],[1.11,2.23]],[[1.11,2.23],[3.11,4.55],[3.14,5.55],[1.11,2.23]]]:
        assert True
    else:
        assert False

def test_get_calculation_area():
    """計算範囲の座標を整数のタプルで出す
    """
    a = u1.get_calculation_area((12.452, 23.556, 1024.521, 2041.241),10)
    assert a == (10, 20, 1030, 2050)

def test_create_10m_mesh_polygons():
    """指定された領域内に10m x 10mのメッシュポリゴンを作成します。
    """
    caluculatin_area = (10, 20, 50, 60)
    a = u1.create_10m_mesh_polygons(caluculatin_area)
    assert a[0] == sp.Polygon([(10, 20),(20, 20),(20, 30),(10, 30),(10, 20)])
    assert a[15] == sp.Polygon([(40, 50),(50,50),(50,60),(40,60),(40,50)])
    with pytest.raises(IndexError):
        a[16]

def test_create_linestring_from_xy_coords():
    xy = [[5,6],[7,8],[10,10]]
    linestring = u1.create_linestring_from_xy_coords(xy)
    assert linestring  == sp.LineString([(5,6),(7,8),(10,10)])

def test_create_polygon_from_xy_coords():
    path = [[0,0],[10,11],[20,1],[0,0]]
    polygon = u1.create_polygon_from_xy_coords(path)
    assert polygon == sp.Polygon([(0,0),(10,11),(20,1),(0,0)])

def test_calculate_composite_influence():
    polygon = sp.Polygon([(400,300),(410,300),(410,310),(400,310),(400,300)])
    linestring = sp.LineString([(156.1362,282.5467),(476.4108,12.7895),(733.8699,48.1356)])
    a_mesh = u1.MeshCell(polygon)
    influence_ratio = a_mesh.calculate_composite_influence(linestring)
    assert a_mesh.distance == 177.494
    assert influence_ratio == 1.0

    polygon = sp.Polygon([(680,660),(690,660),(690,670),(680,670),(680,660)])
    linestring = sp.LineString([(156.1362,282.5467),(476.4108,12.7895),(733.8699,48.1356)])
    a_mesh = u1.MeshCell(polygon)
    influence_ratio = a_mesh.calculate_composite_influence(linestring)
    assert a_mesh.distance == 618.797
    assert influence_ratio == 0.6040

def test_create_index():
    polygon = sp.Polygon([(680,660),(690,660),(690,670),(680,670),(680,660)])
    a_mesh = u1.MeshCell(polygon)
    assert a_mesh.index == (68,66)

    polygon = sp.Polygon([(0,0),(10,0),(10,10),(0,10),(0,0)])
    a_mesh = u1.MeshCell(polygon)
    assert a_mesh.index == (0,0)


def test_meshcell_check_polygon_mesh_intersection():
    path_1 = "./test/autocad_log_2.log"
    path_2 = "./test/autocad_log_3.log"

    parse_1 = u1.parse_autocad_log_for_coordinates(path_1)
    parse_2 = u1.parse_autocad_log_for_coordinates(path_2)

    polygon_1 = u1.create_polygon_from_xy_coords(parse_1[0])
    polygon_2 = u1.create_polygon_from_xy_coords(parse_2[0])

    a_mesh = u1.MeshCell(polygon_1)
    flag = a_mesh.check_polygon_mesh_intersection(polygon_2)

    # print(f"フラグは{flag}")

def test_calculate_inferior_influence():
    polygon = sp.Polygon([(400,300),(410,300),(410,310),(400,310),(400,300)])
    linestring = sp.LineString([(156.1362,282.5467),(476.4108,12.7895),(733.8699,48.1356)])
    a_mesh = u1.MeshCell(polygon)
    influence_ratio = a_mesh.calculate_inferior_influence(linestring)
    assert a_mesh.distance == 177.494
    assert influence_ratio == 0.0

    polygon = sp.Polygon([(680,660),(690,660),(690,670),(680,670),(680,660)])
    linestring = sp.LineString([(156.1362,282.5467),(476.4108,12.7895),(733.8699,48.1356)])
    a_mesh = u1.MeshCell(polygon)
    influence_ratio = a_mesh.calculate_inferior_influence(linestring)
    assert a_mesh.distance == 618.797
    assert influence_ratio == 0.3960

def test_process_autocad_log():
    log_file_path = "./test/10mメッシュに複数のポリゴンがあるテスト用.log"
    template_excel_filename = "./output/様式_操業面積.xlsx"
    output_excel_filename_template = "./output/{base_file_name}.xlsx" # テンプレート文字列を使用

    base_file_name, polygon_list, collection = process_autocad_log(log_file_path)
    assert base_file_name == "10mメッシュに複数のポリゴンがあるテスト用"
    assert list(polygon_list[0].exterior.coords)[0] == (45.2677662247601, 83.1549257050767)
    assert collection.geom_type == 'GeometryCollection'

def test_calculate_mesh_overlaps():
    log_file_path = "./test/10mメッシュに複数のポリゴンがあるテスト用.log"
    template_excel_filename = "./output/様式_操業面積.xlsx"
    output_excel_filename_template = "./output/{base_file_name}.xlsx" # テンプレート文字列を使用

    base_file_name, polygon_list, collection = process_autocad_log(log_file_path)
    csv_of_surveyor_method, sorted_csv_main_list = calculate_mesh_overlaps(polygon_list, collection)
    count = 0
    for i in csv_of_surveyor_method:
        if i[0] == (5,9): # (5,9) に２つのポリゴンがある
            count += 1
    assert count == 2

def test_create_excel_report():
    log_file_path = "./test/10mメッシュに複数のポリゴンがあるテスト用.log"
    template_excel_filename = "./output/様式_操業面積.xlsx"
    output_excel_filename_template = "./output/{base_file_name}.xlsx" # テンプレート文字列を使用

    base_file_name, polygon_list, collection = process_autocad_log(log_file_path)
    csv_of_surveyor_method, sorted_csv_main_list = calculate_mesh_overlaps(polygon_list, collection)
    create_excel_report(base_file_name, csv_of_surveyor_method, sorted_csv_main_list, template_excel_filename, output_excel_filename_template)

