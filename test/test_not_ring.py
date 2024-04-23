import pytest
from utils import *
import glob

area_name = "not_ring"

def test_out_put_file():
    path = glob.glob(f"./out_data/{area_name}.xlsx")
    if path == []:
        assert path == []
    else:
        out_put_file = OutPutFile(area_name)
        print("path=",path)
        assert path ==  ['./out_data/not_ring.xlsx']


def test_load_cad_data_to_lines():
    area_name = "not_ring"
    lines = load_cad_data_to_lines(area_name)
    assert list(lines[0].coords ) ==  [(84.2162740899358, 15.7311285589658), (34.5126338329765,46.3456895868031)]
    base_polygon_for_cal = polygonize(lines)
    assert base_polygon_for_cal.is_empty == True
    
    