from shapely import *
from utils import *
import csv, sys
import openpyxl as px
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, NamedStyle

# グローバル変数の設定
area_name = "test_2"
step = 10

# メイン計算部
lines = load_cad_data_to_lines(area_name)
base_polygon_for_cal = lines_to_polygon(lines)
list_meshes_with_intersection = list_meshes_with_intersection(step, base_polygon_for_cal)
list_mesh_for_inter_calc = list_intersection_for_calc(list_meshes_with_intersection)
data_for_double_calculation = data_for_double_calculation(list_mesh_for_inter_calc)
# print(data_for_double_calculation)
# print(floor(base_polygon_for_cal.bounds[2]/step))

# ワークブック初期化
out_put_file = OutPutFile(area_name)
wb = px.load_workbook(f"./out_data/{area_name}.xlsx")
ws = wb["メッシュ根拠"]
ws.oddFooter.center.text = "Page &[Page] of &N"

# スタイル設定
title_style = NamedStyle(name="title_style")
title_style.alignment = Alignment(shrink_to_fit=True, horizontal="center")
side = Side(border_style="thin",color='FF000000')
border = Border(left=side, right=side,top=side,bottom=side)

#　スタイル名をワークブックへ登録
# wb.add_named_style(title_style)

####################################
row = 1
ws.cell(row=row, column =1, value=area_name)

double_area = 0.0
for a in data_for_double_calculation:
    row += 1
    ws.cell(row=row, column =1, value=f"メッシュ位置{a[0]}")
    row += 1
    t1 = ws.cell(row=row, column=1, value = "Xn")
    t1.style = title_style
    t2 = ws.cell(row=row, column=2, value = "Yn")
    t2.style = title_style
    t3 = ws.cell(row=row, column=3, value="Xn+1-Xn-1")
    t3.style = title_style
    t4 = ws.cell(row=row, column=4, value="Yn*(Xn+1 - Xn-1)")
    t4.style = title_style

    for i,k in enumerate(a[1]):
        if i == 0:
            row += 1
            k1 = ws.cell(row=row, column=1, value=round(k[0],6))
            k2 = ws.cell(row=row, column=2, value=round(k[1],6))
            k3 = ws.cell(row=row, column=3, value=round(a[1][i+1][0]-a[1][i-1][0],6))
            k4 = ws.cell(row=row, column=4, value=round(k[1]*(a[1][i+1][0]-a[1][i-1][0]),6))
            double_area += k[1]*(a[1][i+1][0]-a[1][i-1][0])
        elif i == len(a[1])-1:
            row += 1
            k1 = ws.cell(row=row, column=1, value=round(k[0],6))
            k2 = ws.cell(row=row, column=2, value=round(k[1],6))
            k3 = ws.cell(row=row, column=3, value=round(a[1][0][0]-a[1][i-1][0],6))
            k4 = ws.cell(row=row, column=4, value=round(k[1]*(a[1][0][0]-a[1][i-1][0]),6))
            double_area += k[1]*(a[1][0][0]-a[1][i-1][0])
        else:
            row += 1
            k1 = ws.cell(row=row, column=1, value=round(k[0],6))
            k2 = ws.cell(row=row, column=2, value=round(k[1],6))
            k3 = ws.cell(row=row, column=3, value=round(a[1][i+1][0]-a[1][i-1][0],6))
            k4 = ws.cell(row=row, column=4, value=round(k[1]*(a[1][i+1][0]-a[1][i-1][0]),6))
            # print("i=",i,"Xn=",k[0],"Yn=",k[1],"Xn+1 - Xn-1=",a[1][i+1][0]-a[1][i-1][0],"Yn*(Xn+1 - Xn-1)=",k[1]*(a[1][i+1][0]-a[1][i-1][0]))
            double_area += k[1]*(a[1][i+1][0]-a[1][i-1][0])
    row += 1
    sum1 = ws.cell(row=row, column=3, value="倍面積")
    sum2 = ws.cell(row=row, column=4, value=round(double_area,6))
    row += 1
    sum1 = ws.cell(row=row, column=3, value="面積")
    sum2 = ws.cell(row=row, column=4, value=round(double_area/2,6))
    # print(f"{a[0]}area =",round(double_area/2,6))
    double_area = 0.0

# 全体に罫線を入れる
for r in range(2, row+1):
    for c in range(1,5):
        ts = ws.cell(row=r, column=c)
        ts.border = border

# 操業範囲のシート設定
ws = wb["操業範囲"]

# 面積が0以外の一覧表を作る
list_mesh_without0 = []
row = 4
for mesh in list_meshes_with_intersection:
    area = mesh.intersection().area
    if not area == 0.0:
        row += 1
        ws.cell(row=row, column=3, value=mesh.index_x)
        ws.cell(row=row, column=4, value=mesh.index_y)
        sum_s = ws.cell(row=row, column=5, value=round(area,6))
        if not area == 100:
            sum_s.number_format = "0.000000"
sum_top = ws.cell(row=4, column=5, value=f"=sum(E5:E{row})")
sum_top.number_format = "0.000000"

# 保存
wb.save(f"./out_data/{area_name}.xlsx")
