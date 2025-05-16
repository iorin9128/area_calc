import csv
from shapely.geometry import Polygon
from decimal import Decimal, ROUND_HALF_UP

def calculate_polygon_area_surveyor_method(polygon: Polygon):
    # テスト作成済
    
    coords_raw = list(polygon.exterior.coords)
    
    if len(coords_raw) > 1 and coords_raw[0] == coords_raw[-1]:
        coords = coords_raw[:-1]
    else:
        coords = coords_raw

    num_coords = len(coords)

    calculated_data = {}
    temp = []
    double_area = 0.0

    for i in range(num_coords):
        xn = coords[i][0]
        yn = coords[i][1]
        y_plus_1 = coords[(i + 1) % num_coords][1]
        y_minus_1 = coords[(i - 1 + num_coords) % num_coords][1]
        diff_y = y_plus_1 - y_minus_1
        term = xn * diff_y
                 
        temp.append(
            [round(xn, 6),
             round(yn, 6),
             round(diff_y, 6),
             round(term, 6)]
            )
        double_area += term

    area = abs(double_area / 2.0)
    calculated_data["data_list"] = temp
    calculated_data["double_area"] = round(double_area, 6)
    calculated_data["area"] = round(area, 6)

    return calculated_data