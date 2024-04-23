import pytest
from utils import *
import glob

area_name = "test_2"

def test_out_put_file():
    path = glob.glob(f"./out_data/{area_name}.xlsx")
    if path == []:
        assert path == []
    else:
        out_put_file = OutPutFile(area_name)
        print("path=",path)
        assert path ==  ['./out_data/test_2.xlsx']


def test_load_cad_data_to_lines():
    area_name = "test_2"
    lines = load_cad_data_to_lines(area_name)
    assert list(lines[0].coords ) ==  [(84.2162740899358, 15.7311285589658), (34.5126338329765,46.3456895868031)]
    base_polygon_for_cal = polygonize(lines)
    print(lines)
    assert base_polygon_for_cal.geom_type == "GeometryCollection"
    assert list(list(base_polygon_for_cal.geoms)[0].boundary.coords)[0] == (84.2162740899358,15.7311285589658)

