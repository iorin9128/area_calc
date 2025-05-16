import shapely.geometry
import math
from typing import Optional # Optional型ヒントのため

def find_point_vertically_within_distance(
    line: shapely.geometry.LineString,
    point: shapely.geometry.Point,
    max_distance: float,
    step_factor: float = 1.0, # 距離差に基づくステップサイズの調整係数
    min_step: float = 1e-6,    # y座標の最小増加量
    max_iterations: int = 500  # 無限ループ防止のための最大試行回数
) -> Optional[shapely.geometry.Point]: # PointオブジェクトまたはNoneを返す
    """
    指定されたLineStringからの距離がmax_distance以下になるように、
    指定されたPointのy座標を増加させて新しいPointを探します。

    Args:
        line: 基準となるLineString。
        point: 開始点 (LineStringより下にあると仮定)。x座標は変更されません。
        max_distance: 目標とする最大距離。
        step_factor: 現在距離と目標距離の差に掛ける係数。ステップサイズを調整します。
                     1.0 前後が基本。小さい値ほど慎重に、大きい値ほど大胆に探索します。
        min_step: 1回の繰り返しでのy座標の最小増加量。非常に近い場合の停滞を防ぎます。
        max_iterations: 探索の最大繰り返し回数。

    Returns:
        条件を満たす新しいPointオブジェクト。max_iterations以内に見つからなかった場合はNone。
    """
    if not isinstance(line, shapely.geometry.LineString):
        raise TypeError("line must be a shapely LineString")
    if not isinstance(point, shapely.geometry.Point):
        raise TypeError("point must be a shapely Point")
    if max_distance < 0:
        raise ValueError("max_distance cannot be negative")

    x = point.x
    current_y = point.y
    current_point = shapely.geometry.Point(x, current_y)

    # Shapely 2.0以降では line.distance(point) が推奨される
    current_dist = line.distance(current_point)
    # print(f"Initial state: y={current_y:.4f}, distance={current_dist:.4f}") # デバッグ用

    # 開始時点ですでに条件を満たしている場合
    if current_dist <= max_distance:
        # print("Initial point already satisfies the condition.")
        return current_point

    iterations = 0
    while current_dist > max_distance and iterations < max_iterations:
        iterations += 1

        # 目標距離までの差を計算
        distance_to_reduce = current_dist - max_distance

        # y座標の増加量を計算 (距離の差に比例させる + 最小ステップ保証)
        y_increase = max(min_step, distance_to_reduce * step_factor)

        # y座標を更新
        current_y += y_increase
        current_point = shapely.geometry.Point(x, current_y)

        # 新しい距離を計算
        last_dist = current_dist # デバッグや分析用に前の距離を保持可能
        current_dist = line.distance(current_point)

        # print(f"Iter {iterations}: y={current_y:.4f}, dist={current_dist:.4f}, y_inc={y_increase:.4f}") # デバッグ用

    # ループ終了後の結果確認
    if current_dist <= max_distance:
        # print(f"Found point within distance after {iterations} iterations.")
        return current_point
    else:
        # print(f"Warning: Could not find point within {max_iterations} iterations.")
        # print(f"Last state: y={current_y:.4f}, distance={current_dist:.4f} (target <= {max_distance})")
        return None # 見つからなかった場合はNoneを返す
