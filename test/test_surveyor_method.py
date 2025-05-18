import pytest
from surveyor_method import *
import utils_1 as u1

def test_surveyor_method():
    path = "./test/autocad_log_3.log"
    parsers = u1.parse_autocad_log_for_coordinates(path)
    # print("test_surveyor_method",a)
    u1.append_first_to_end_if_mismatched(parsers)
    polygon_list = []
    for l in parsers:
        polygon_list.append(u1.create_polygon_from_xy_coords(l))
    test_data = calculate_polygon_area_surveyor_method(polygon = polygon_list[0])
    assert test_data["data_list"][0] == [39.5433, -15.5553, 20.0488, 792.795713]
    assert test_data["double_area"] == -706.907123
    assert test_data["area"] == 353.453561