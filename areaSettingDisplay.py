import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches
import os

# 定義されたデータ
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
            "domain_lowerLimitOfZ(m)": -0.7,
            "domain_upperLimitOfX(m)": 1.5,
            "domain_upperLimitOfY(m)": 1.0,
            "domain_upperLimitOfZ(m)": 0.7,
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
    "CCC": "#2ca02c",  # 緑
}

# データセットごとの透明度
dataset_alpha = {
    "05_LambdaByLIs1.0_lowReso_smooth": {"AAA": 0.4, "BBB": 0.6, "CCC": 0.8},
    "06_LambdaByLIs1.0_lowReso_smooth_moreDetail": {"AAA": 0.3, "BBB": 0.5, "CCC": 0.7},
}

def create_box(ax, limits, color, label, alpha):
    """
    指定された範囲でボックスを作成し、3Dプロットに追加します。
    """
    x_min = limits["domain_lowerLimitOfX(m)"]
    x_max = limits["domain_upperLimitOfX(m)"]
    y_min = limits["domain_lowerLimitOfY(m)"]
    y_max = limits["domain_upperLimitOfY(m)"]
    z_min = limits["domain_lowerLimitOfZ(m)"]
    z_max = limits["domain_upperLimitOfZ(m)"]

    # ボックスの8頂点
    vertices = [
        [x_min, y_min, z_min],
        [x_max, y_min, z_min],
        [x_max, y_max, z_min],
        [x_min, y_max, z_min],
        [x_min, y_min, z_max],
        [x_max, y_min, z_max],
        [x_max, y_max, z_max],
        [x_min, y_max, z_max]
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

    box = Poly3DCollection(faces, linewidths=1.5, edgecolors='k')  # 輪郭線を太く設定
    box.set_facecolor(color)
    box.set_alpha(alpha)  # 各領域ごとの透明度設定
    ax.add_collection3d(box)

    # テキストの配置（ボックスの中心）
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    center_z = (z_min + z_max) / 2
    annotation = (
        f"{label}\n"
        f"X: [{x_min}, {x_max}]\n"
        f"Y: [{y_min}, {y_max}]\n"
        f"Z: [{z_min}, {z_max}]"
    )
    ax.text(center_x, center_y, z_max, annotation, color='black', fontsize=8, ha='center', zorder=10)

# プロットの生成と保存
for dataset_name, regions in datasets.items():
    # プロットのセットアップ
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # プロット順序を指定（大きい領域から小さい領域へ）
    plot_order = ["AAA", "BBB", "CCC"]

    for region in plot_order:
        if region in regions:
            limits = regions[region]
            color = region_colors.get(region, "gray")
            alpha = dataset_alpha.get(dataset_name, {}).get(region, 0.5)
            create_box(ax, limits, color, region, alpha)

    # 軸ラベルの設定
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_zlabel('Z (m)', fontsize=12)

    # タイトルの設定
    ax.set_title(f'{dataset_name} の領域表示', fontsize=15)

    # 凡例の作成
    patches = [mpatches.Patch(color=region_colors[region], label=region) for region in plot_order]
    ax.legend(handles=patches, loc='upper left')

    # 軸の範囲を自動調整
    all_x = []
    all_y = []
    all_z = []
    for limits in regions.values():
        all_x.extend([limits["domain_lowerLimitOfX(m)"], limits["domain_upperLimitOfX(m)"]])
        all_y.extend([limits["domain_lowerLimitOfY(m)"], limits["domain_upperLimitOfY(m)"]])
        all_z.extend([limits["domain_lowerLimitOfZ(m)"], limits["domain_upperLimitOfZ(m)"]])

    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
    ax.set_zlim(min(all_z) - 1, max(all_z) + 1)

    # グリッドの表示
    ax.grid(True)

    # ビューポイントの設定（視点を調整して重なりを減らす）
    ax.view_init(elev=20, azim=30)  # 仰角20度、方位角30度

    # ファイル名の設定（実行ディレクトリに保存）
    filename = f"{dataset_name}.png"
    filepath = os.path.join(os.getcwd(), filename)

    # 画像の保存
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"{filename} を保存しました。")

    # プロットを閉じてメモリを解放
    plt.close(fig)

print("全ての画像の保存が完了しました。")
