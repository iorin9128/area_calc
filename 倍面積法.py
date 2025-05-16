import csv
from shapely.geometry import Polygon, LinearRing

def calculate_polygon_area_steps_to_csv_formatted_with_summary(polygon: Polygon, csv_filename: str) -> float:
    """
    ShapelyのPolygonオブジェクトの面積を倍面積法で計算し、
    計算過程と最終的な倍面積・面積を指定フォーマットでCSVファイルに出力します。

    Args:
        polygon: 面積を計算するShapelyのPolygonまたはLinearRingオブジェクト。
        csv_filename: 計算過程と結果を出力するCSVファイル名。

    Returns:
        計算されたポリゴンの面積（小数点第6位まで）。

    Raises:
        TypeError: 入力がPolygonまたはLinearRingでない場合。
        ValueError: ポリゴンが3頂点未満の場合。
        IOError: CSVファイルへの書き込み中にエラーが発生した場合。

    CSV列 (フォーマット済み):
        X: 頂点のX座標 (小数点第3位まで)
        Y: 頂点のY座標 (小数点第3位まで)
        Xn+1 - Xn-1: 次の頂点のX座標から前の頂点のX座標を引いた値 (小数点第6位まで)
                       または '倍面積', '面積' ラベル
        Yn * (Xn+1 - Xn-1): Y座標と上記の差の積 (倍面積の各項) (小数点第6位まで)
                           または 対応する倍面積合計、面積値 (小数点第6位まで)
    """
    if not isinstance(polygon, (Polygon, LinearRing)):
        raise TypeError("Input must be a Shapely Polygon or LinearRing object.")

    # Polygonの場合はexterior（外周）の座標、LinearRingの場合はそのまま座標を取得
    if isinstance(polygon, Polygon):
        coords = list(polygon.exterior.coords)
    else: # LinearRing
        coords = list(polygon.coords)

    # Shapelyは始点と終点を重複して格納するため、最後の点を削除して処理
    if len(coords) > 1 and coords[0] == coords[-1]:
        coords = coords[:-1]

    n = len(coords)
    if n < 3:
        raise ValueError("Polygon must have at least 3 vertices.")

    csv_data = []
    double_area_sum = 0.0 # 計算中は高精度で保持

    print(f"Calculating area for polygon with {n} vertices.")

    for i in range(n):
        x_i, y_i = coords[i]
        x_next = coords[(i + 1) % n][0]
        x_prev = coords[(i - 1 + n) % n][0]
        delta_x = x_next - x_prev
        term = y_i * delta_x
        double_area_sum += term

        # CSVデータ行を作成 (指定桁数にフォーマット)
        row = [
            f"{x_i:.3f}",
            f"{y_i:.3f}",
            f"{delta_x:.6f}",
            f"{term:.6f}"
        ]
        csv_data.append(row)

    # 面積の計算 (倍面積の絶対値を2で割り、小数点第6位に丸める)
    # 倍面積合計自体も小数点第6位に丸める（CSV出力用）
    formatted_double_area_sum = round(double_area_sum, 6)
    area = round(abs(double_area_sum) / 2.0, 6)

    print(f"Double Area Sum (raw) = {double_area_sum}")
    print(f"Double Area Sum (rounded to 6 decimal places) = {formatted_double_area_sum:.6f}")
    print(f"Calculated Area (rounded to 6 decimal places) = {area:.6f}")

    # CSVファイルへの書き込み
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # ヘッダー行の書き込み
            writer.writerow(['Xn', 'Yn', 'Xn+1 - Xn-1', 'Yn * (Xn+1 - Xn-1)'])
            # データ行の書き込み
            writer.writerows(csv_data)

            # --- 追加行の書き込み ---
            # 空行を1行追加（任意、見やすくするため）
            # writer.writerow([])

            # 倍面積の行
            writer.writerow([
                '',                     # X列は空
                '',                     # Y列は空
                '倍面積',               # ラベル
                f"{formatted_double_area_sum:.6f}" # 計算された倍面積合計（フォーマット済み）
            ])

            # 面積の行
            writer.writerow([
                '',                     # X列は空
                '',                     # Y列は空
                '面積',                 # ラベル
                f"{area:.6f}"           # 計算された面積（フォーマット済み）
            ])
            # --- 追加行ここまで ---

        print(f"Calculation steps and summary (formatted) saved to '{csv_filename}'")
    except IOError as e:
        print(f"Error writing to CSV file '{csv_filename}': {e}")
        raise

    return area

# --- 使用例 ---
# 前回の例と同じポリゴンを使用
polygon_float = Polygon([(0.123, 0.567), (10.987, 0.111), (10.555, 10.444), (0.876, 10.123)])
output_csv_filename_summary = 'polygon_area_summary.csv'
calculated_area_summary = calculate_polygon_area_steps_to_csv_formatted_with_summary(
    polygon_float, output_csv_filename_summary
)

print(f"\n最終的に計算された面積 (小数点第6位まで): {calculated_area_summary:.6f}")

# --- Shapelyの面積と比較 ---
print(f"Shapelyによる面積計算結果: {polygon_float.area:.6f}")

# CSVファイル 'polygon_area_summary.csv' を確認してください。
# 末尾に倍面積と面積の行が追加されているはずです。