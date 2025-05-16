import pytest
from surveyor_method import *
from utils_1 import *

def test_surveyor_method():
    path = "./test/autocad_log_3.log"
    parsers = parse_autocad_log_for_coordinates(path)
    # print("test_surveyor_method",a)
    append_first_to_end_if_mismatched(parsers)
    polygon_list = []
    for l in parsers:
        polygon_list.append(create_polygon_from_xy_coords(l))
    test_data = calculate_polygon_area_surveyor_method(polygon = polygon_list[0])
    assert test_data["data_list"][0] == [39.5433, -15.5553, 20.0488, 792.795713]
    assert test_data["double_area"] == -706.907123
    assert test_data["area"] == 353.453561