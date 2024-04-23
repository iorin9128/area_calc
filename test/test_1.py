import pytest
from utils import *
import glob

area_name = "test_1"

def test_out_put_file():
    path = glob.glob(f"./out_data/{area_name}.xlsx")
    if path == []:
        assert path == []
    else:
        out_put_file = OutPutFile(area_name)
        print("path=",path)
        assert path ==  ['./out_data/test_1.xlsx']


def test_load_cad_data_to_lines():
    area_name = "test_1"
    lines = load_cad_data_to_lines(area_name)
    assert list(lines[0].coords ) ==  [(14.8570663811563, 14.6769807280514), (23.1410064239829, 26.2925053533191)]
    base_polygon_for_cal = polygonize(lines)
    assert base_polygon_for_cal.geom_type == "GeometryCollection"
    assert list(list(base_polygon_for_cal.geoms)[0].boundary.coords)[0] == (14.8570663811563, 14.6769807280514)
    