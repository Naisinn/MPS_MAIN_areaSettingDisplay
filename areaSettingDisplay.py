import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import os

# 日本語フォントの設定
def set_japanese_font():
    # フォント名を指定
    font_name = 'Noto Sans JP'
    # フォントパスを取得
    font_paths = [f.fname for f in fm.fontManager.ttflist if font_name in f.name]
    
    if font_paths:
        # フォントが見つかった場合、最初のパスを使用
        font_path = font_paths[0]
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = font_name
        print(f"日本語フォント '{font_name}' を使用します。")
    else:
        # フォントが見つからない場合、デフォルトのフォントを使用
        plt.rcParams['font.family'] = 'sans-serif'
        print(f"指定した日本語フォント '{font_name}' が見つかりません。デフォルトのフォントを使用します。")

set_japanese_font()

# データセット定義
datasets = {
    "05_LambdaByLIs1.0_lowReso_smooth": {
        "AAA": {
            "distanceBetweenParticles(m)": 0.05,
            "domain_lowerLimitOfX(m)": -2.5,
            "domain_lowerLimitOfY(m)": -1.50,
            "domain_lowerLimitOfZ(m)": -1.3,
            "domain_upperLimitOfX(m)": 2.0,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 1.3,
        },
        "BBB": {
            "distanceBetweenParticles(m)": 0.03,
            "domain_lowerLimitOfX(m)": -1.0,
            "domain_lowerLimitOfY(m)": -0.9,
            "domain_lowerLimitOfZ(m)": -0.7,
            "domain_upperLimitOfX(m)": 1.5,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 0.7,
        },
        "CCC": {
            "distanceBetweenParticles(m)": 0.02,
            "domain_lowerLimitOfX(m)": -0.35,
            "domain_lowerLimitOfY(m)": -0.50,
            "domain_lowerLimitOfZ(m)": -0.280,
            "domain_upperLimitOfX(m)": 0.5,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 0.28,
        },
    },
    "06_LambdaByLIs1.0_lowReso_smooth_moreDetail": {
        "AAA": {
            "distanceBetweenParticles(m)": 0.03,
            "domain_lowerLimitOfX(m)": -2.5,
            "domain_lowerLimitOfY(m)": -1.50,
            "domain_lowerLimitOfZ(m)": -2.6,
            "domain_upperLimitOfX(m)": 2.0,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 2.6,
        },
        "BBB": {
            "distanceBetweenParticles(m)": 0.015,
            "domain_lowerLimitOfX(m)": -1.5,
            "domain_lowerLimitOfY(m)": -0.9,
            "domain_lowerLimitOfZ(m)": -1.4,
            "domain_upperLimitOfX(m)": 1.5,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 1.4,
        },
        "CCC": {
            "distanceBetweenParticles(m)": 0.0075,
            "domain_lowerLimitOfX(m)": -0.525,
            "domain_lowerLimitOfY(m)": -0.50,
            "domain_lowerLimitOfZ(m)": -0.56,
            "domain_upperLimitOfX(m)": 0.5,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 0.56,
        },
    }
}

# カラーマップの定義（各領域ごとに異なる色）
region_colors = {
    "AAA": "#1f77b4",  # 青
    "BBB": "#ff7f0e",  # オレンジ
    "CCC": "#d62728",  # 赤（視認性向上のため変更）
}

# データセットごとの透明度
dataset_alpha = {
    "05_LambdaByLIs1.0_lowReso_smooth": {"AAA": 0.4, "BBB": 0.6, "CCC": 0.8},
    "06_LambdaByLIs1.0_lowReso_smooth_moreDetail": {"AAA": 0.3, "BBB": 0.5, "CCC": 0.7},
}

def create_box(ax, limits, color, label, alpha):
    """
    元データ: X, Y, Z
    表示時は (X, Z, Y) でプロットする:
      - プロットのX軸 <- 元X
      - プロットのY軸 <- 元Z
      - プロットのZ軸 <- 元Y

    これで表示上はY軸が垂直方向として機能します。
    """
    # 元データ
    x_min = limits["domain_lowerLimitOfX(m)"]
    x_max = limits["domain_upperLimitOfX(m)"]
    y_min = limits["domain_lowerLimitOfY(m)"]
    y_max = limits["domain_upperLimitOfY(m)"]
    z_min = limits["domain_lowerLimitOfZ(m)"]
    z_max = limits["domain_upperLimitOfZ(m)"]

    # 表示データに変換 (X, Z, Y)
    X_coords = [x_min, x_max]
    Y_coords = [z_min, z_max]  # 元ZがプロットYへ
    Z_coords = [y_min, y_max]  # 元YがプロットZへ

    # ボックスの8頂点を定義
    vertices = [
        [X_coords[0], Y_coords[0], Z_coords[0]],
        [X_coords[1], Y_coords[0], Z_coords[0]],
        [X_coords[1], Y_coords[1], Z_coords[0]],
        [X_coords[0], Y_coords[1], Z_coords[0]],
        [X_coords[0], Y_coords[0], Z_coords[1]],
        [X_coords[1], Y_coords[0], Z_coords[1]],
        [X_coords[1], Y_coords[1], Z_coords[1]],
        [X_coords[0], Y_coords[1], Z_coords[1]]
    ]

    # ボックスの6面を定義
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # 下面
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # 上面
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # 前面
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # 背面
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # 右側面
        [vertices[4], vertices[7], vertices[3], vertices[0]],  # 左側面
    ]

    # 輪郭線の強調
    if label == "CCC":
        linewidth = 2.5
        edgecolor = 'black'
    else:
        linewidth = 1.5
        edgecolor = 'k'

    box = Poly3DCollection(faces, linewidths=linewidth, edgecolors=edgecolor)
    box.set_facecolor(color)
    box.set_alpha(alpha)
    ax.add_collection3d(box)

    # 注釈のフォントサイズと配置
    box_size = max((x_max - x_min), (Y_coords[1] - Y_coords[0]), (Z_coords[1] - Z_coords[0]))
    base_font_size = 8
    font_size = max(8, min(base_font_size * (box_size / 1.0), 12))

    # ボックスの中心
    center_x = (x_min + x_max) / 2
    center_y = (Y_coords[0] + Y_coords[1]) / 2
    center_z = (z_min + z_max) / 2

    # テキストのオフセットを調整して重なりを防止
    if label == "CCC":
        text_offset = 0.1 * box_size
    else:
        text_offset = 0.05 * box_size

    annotation = (
        f"{label}\n"
        f"X: [{x_min}, {x_max}]\n"
        f"Y: [{y_min}, {y_max}]\n"
        f"Z: [{z_min}, {z_max}]"
    )

    # テキストをボックスの上に配置し、オフセットを適用
    ax.text(center_x, Y_coords[1] + text_offset, center_z, annotation,
            color='black', fontsize=font_size, ha='center', zorder=10,
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

# 軸範囲計算
all_x, all_y, all_z = [], [], []
for dataset in datasets.values():
    for limits in dataset.values():
        x_min = limits["domain_lowerLimitOfX(m)"]
        x_max = limits["domain_upperLimitOfX(m)"]
        y_min = limits["domain_lowerLimitOfY(m)"]
        y_max = limits["domain_upperLimitOfY(m)"]
        z_min = limits["domain_lowerLimitOfZ(m)"]
        z_max = limits["domain_upperLimitOfZ(m)"]

        # 表示データに変換 (X, Z, Y)
        all_x.extend([x_min, x_max])
        all_y.extend([z_min, z_max])  # 元ZがプロットYへ
        all_z.extend([y_min, y_max])  # 元YがプロットZへ

# 軸範囲を統一
x_min_global = min(all_x) - 1
x_max_global = max(all_x) + 1
y_min_global = min(all_y) - 1
y_max_global = max(all_y) + 1
z_min_global = min(all_z) - 1
z_max_global = max(all_z) + 1

# プロットの生成と保存
fig = plt.figure(figsize=(28, 12))  # 横に広い図を作成

for i, (dataset_name, regions) in enumerate(datasets.items(), 1):
    ax = fig.add_subplot(1, 2, i, projection='3d')

    # プロット順序を指定（大きい領域から小さい領域へ）
    plot_order = ["AAA", "BBB", "CCC"]

    for region in plot_order:
        if region in regions:
            limits = regions[region]
            color = region_colors.get(region, "gray")
            alpha = dataset_alpha.get(dataset_name, {}).get(region, 0.5)
            create_box(ax, limits, color, region, alpha)

    # 軸ラベルの設定
    ax.set_xlabel('X (m)', fontsize=14)
    ax.set_ylabel('Z (m)', fontsize=14)  # 元ZがプロットYへ
    ax.set_zlabel('Y (m) (垂直)', fontsize=14)  # 元YがプロットZへ、垂直方向

    # タイトルの設定
    ax.set_title(f'{dataset_name} の領域表示', fontsize=18)

    # 凡例の作成（最初のサブプロットでのみ作成）
    if i == 1:
        patches = [mpatches.Patch(color=region_colors[r], label=r) for r in plot_order]
        ax.legend(handles=patches, loc='upper left', fontsize=12)

    # 軸の範囲を統一
    ax.set_xlim(x_min_global, x_max_global)
    ax.set_ylim(y_min_global, y_max_global)
    ax.set_zlim(z_min_global, z_max_global)

    # グリッドの表示
    ax.grid(True, linestyle='--', linewidth=0.5, color='gray')

    # ビューポイントの設定（視点を統一）
    ax.view_init(elev=20, azim=30)  # 仰角20度、方位角30度

# レイアウトの調整
plt.tight_layout()

# ファイル名の設定（実行ディレクトリに保存）
filename = "combined_datasets.png"
filepath = os.path.join(os.getcwd(), filename)

# 画像の保存
plt.savefig(filepath, dpi=300, bbox_inches='tight')
print(f"{filename} を保存しました。")

# プロットを閉じてメモリを解放
plt.close(fig)

print("画像の保存が完了しました。")
