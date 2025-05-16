import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # FontPropertiesをインポート

# --- FontProperties の設定 ---
# 環境に合わせて以下のいずれかの方法を選択してください

# 方法1: フォントファイルのフルパスを指定 (最も確実)
# ご自身の環境にあるフォントファイルのパスに置き換えてください。
# 例: WindowsでMS Gothicを指定する場合 (ファイル名やパスは環境により異なります)
font_path = 'C:\Windows\Fonts\msgothic.ttc'
# 例: macOSでヒラギノ角ゴシックを指定する場合
# font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc' # 正確なパスを確認してください
# 例: LinuxでIPAexGothicを指定する場合 (インストールされている場合)
# font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf' # パスは環境により異なります

try:
    # FontPropertiesオブジェクトを作成
    jp_font_prop = FontProperties(fname=font_path)
    print(f"指定されたフォントパス '{font_path}' を使用します。")
except FileNotFoundError:
    print(f"警告: 指定されたフォントパス '{font_path}' が見つかりません。")
    # フォールバックとして、システムが認識できるフォントファミリー名を試す
    # (この方法は環境依存性が高いため、パス指定が推奨されます)
    try:
        # 例: Windows, macOS, Linuxで共通して存在しやすいフォントファミリー
        # ただし、必ずしも日本語が表示できるとは限りません。
        # 適切な日本語フォントファミリー名に変更してください。
        font_family_name = "IPAexGothic" # または "Yu Gothic", "MS Gothic", "Hiragino Sans" など
        jp_font_prop = FontProperties(family=font_family_name)
        print(f"フォントファミリー名 '{font_family_name}' を使用します。")
    except:
        print(f"警告: フォントファミリー '{font_family_name}' も見つかりません。デフォルトフォントで描画します（文字化けの可能性あり）。")
        jp_font_prop = FontProperties() # デフォルトフォント


# --- NetworkX グラフ作成 ---
G = nx.DiGraph()
people = ["Aさん", "Bさん", "Cさん", "Dさん", "Eさん", "Fさん"]
G.add_nodes_from(people)

parent_child_relationships = [
    ("Aさん", "Bさん"),
    ("Aさん", "Cさん"),
    ("Bさん", "Dさん"),
    ("Bさん", "Eさん"),
    ("Cさん", "Fさん")
]
G.add_edges_from(parent_child_relationships)

# --- グラフの可視化 ---
plt.figure(figsize=(10, 7)) # 少し大きめに
pos = nx.spring_layout(G, seed=42, k=0.8) # kパラメータでノード間隔を調整

# nx.drawのラベルにFontPropertiesを適用
# node_labels = {node: node for node in G.nodes()} # ラベル辞書を作成
nx.draw_networkx_nodes(G, pos, node_size=2500, node_color="skyblue")
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=20, edge_color='gray')

# ラベル描画時にfont_familyやfontpropertiesを指定できますが、
# matplotlibのグローバル設定を変更する方が簡単な場合もあります。
# ここでは、各ラベルにFontPropertiesを適用します。
for node, (x, y) in pos.items():
    plt.text(x, y, node, fontproperties=jp_font_prop, fontsize=10, ha='center', va='center')

# タイトルにもFontPropertiesを適用
plt.title("親子関係のネットワーク図 (FontProperties使用)", fontproperties=jp_font_prop, fontsize=16)
plt.axis('off') # 軸を非表示
plt.show()

# --- 関係性の確認 ---
print("\n関係性の確認:")
if G.has_node("Aさん"):
    print(f"Aさんの子供たち: {list(G.successors('Aさん'))}")
if G.has_node("Dさん"):
    print(f"Dさんの親: {list(G.predecessors('Dさん'))}")
if G.has_edge("Bさん", "Eさん"):
    print("BさんはEさんの親です。")