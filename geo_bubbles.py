import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
import math
from scipy.optimize import minimize

# 设置中文字体支持
# 尝试加载常见的中文字体
try:
    # 尝试使用微软雅黑
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    # 增大全局字体大小
    plt.rcParams['font.size'] = 16  # 默认字体大小增大
    print("已设置中文字体")
except:
    print("警告: 无法设置中文字体，可能导致中文显示为方块")

# 读取数据
file_path = 'STOXX_geo.xlsx'
data = pd.read_excel(file_path)
print("原始列名:", data.columns)
print("原始数据示例:\n", data.head())

# 假设国家名称在'COUNTRY'列，权重在'Weightings'列
# 如果列名不同，请根据实际情况修改
try:
    # 尝试直接使用列名
    country_column = 'COUNTRY'
    weight_column = 'Weightings'
    
    # 按国家计算权重
    country_weights = data.groupby(country_column)[weight_column].sum().reset_index()
    
except KeyError:
    # 如果找不到列名，尝试使用位置索引
    print("未找到指定列名，尝试使用位置索引...")
    # 假设国家在第一列，权重在第二列
    country_column = data.columns[0]
    weight_column = data.columns[1]
    
    # 按国家计算权重
    country_weights = data.groupby(country_column)[weight_column].sum().reset_index()

print("国家权重数据:\n", country_weights)

# 将权重数据转换为数值类型（如果不是的话）
if not pd.api.types.is_numeric_dtype(country_weights[weight_column]):
    # 如果权重包含百分比符号，先去除
    if country_weights[weight_column].dtype == 'object':
        country_weights[weight_column] = country_weights[weight_column].str.rstrip('%').astype('float') / 100
    else:
        country_weights[weight_column] = pd.to_numeric(country_weights[weight_column], errors='coerce')

# 按权重从大到小排序
country_weights = country_weights.sort_values(by=weight_column, ascending=False)

# 国家名称英文转中文映射（根据需要扩展）
country_translation = {
    'Germany': '德国',
    'France': '法国',
    'United Kingdom': '英国',
    'Switzerland': '瑞士',
    'Netherlands': '荷兰',
    'Sweden': '瑞典',
    'Spain': '西班牙',
    'Italy': '意大利',
    'Denmark': '丹麦',
    'Finland': '芬兰',
    'Belgium': '比利时',
    'Norway': '挪威',
    'Ireland': '爱尔兰',
    'Austria': '奥地利',
    'Portugal': '葡萄牙',
    'Luxembourg': '卢森堡',
    'Greece': '希腊',
    'Poland': '波兰',
    'Czech Republic': '捷克',
    'Hungary': '匈牙利',
    'Russia': '俄罗斯',
    'Turkey': '土耳其',
    'United States': '美国',
    'Canada': '加拿大',
    'Japan': '日本',
    'China': '中国',
    'Hong Kong': '香港',
    'Taiwan': '台湾',
    'South Korea': '韩国',
    'Australia': '澳大利亚',
    'New Zealand': '新西兰',
    'Singapore': '新加坡',
    'India': '印度',
    'Brazil': '巴西',
    'South Africa': '南非'
}

# 添加中文国家名称列
country_weights['国家'] = country_weights[country_column].map(lambda x: country_translation.get(x, x))
print("添加中文名称后的数据:\n", country_weights)

# 设置气泡大小，使用非线性映射确保小权重的气泡不会过大
# 使用平方根映射，这样面积与权重成正比
max_weight = country_weights[weight_column].max()
min_weight = country_weights[weight_column].min()

# 设置最小和最大气泡半径
min_radius = 0.3  # 最小气泡半径
max_radius = 3.0  # 最大气泡半径

# 计算气泡半径，使用平方根映射确保面积与权重成正比
country_weights['radius'] = country_weights[weight_column].apply(
    lambda w: min_radius + (max_radius - min_radius) * np.sqrt((w - min_weight) / (max_weight - min_weight))
)

# 打印权重和对应的半径
print("\n权重和对应的半径:")
for i, (country, weight, radius) in enumerate(zip(
    country_weights[country_column], 
    country_weights[weight_column],
    country_weights['radius']
)):
    print(f"{country}: 权重 = {weight:.2%}, 半径 = {radius:.2f}")

# 获取半径数组
radii = country_weights['radius'].values

# 根据权重分组，将权重分为几个区间，相同区间使用相同颜色
# 定义权重区间
weight_bins = [0, 0.02, 0.05, 0.10, 0.15, 1.0]
weight_labels = ['0-2%', '2-5%', '5-10%', '10-15%', '15%+']
country_weights['weight_group'] = pd.cut(country_weights[weight_column], bins=weight_bins, labels=weight_labels)

# 为每个权重组分配颜色
color_map = {
    '0-2%': '#8dd3c7',
    '2-5%': '#ffffb3',
    '5-10%': '#bebada',
    '10-15%': '#fb8072',
    '15%+': '#80b1d3'
}
country_weights['color'] = country_weights['weight_group'].map(color_map)

# 为每个气泡分配字体大小，权重越大字体越大（增大两倍）
min_font_size = 14  # 原来是7，增大两倍
max_font_size = 28  # 原来是14，增大两倍
country_weights['font_size'] = country_weights[weight_column].apply(
    lambda w: min_font_size + (max_font_size - min_font_size) * ((w - min_weight) / (max_weight - min_weight))
)

# 使用改进的布局算法，让外围小气泡紧贴在一起并向中心靠拢，同时避免与中间大气泡重叠
def improved_layout(radii, padding=1.0, center_padding=1.2):
    n = len(radii)
    positions = np.zeros((n, 2))
    
    # 第一个气泡（最大的）放在中心
    positions[0] = [0, 0]
    center_radius = radii[0]
    
    if n > 1:
        # 计算剩余气泡的总面积
        remaining_area = sum([np.pi * r**2 for r in radii[1:]])
        
        # 估计所有小气泡围绕中心气泡所需的圆环半径
        # 中心气泡外围的圆环面积应该大致等于所有小气泡的总面积
        ring_inner_radius = center_radius * center_padding  # 内圆半径，稍大于中心气泡半径
        ring_area = remaining_area * 1.5  # 增加一些空间，避免过度拥挤
        ring_outer_radius = np.sqrt(ring_area / np.pi + ring_inner_radius**2)
        
        # 计算平均角度间隔
        angle_step = 2 * np.pi / (n - 1)
        
        # 放置剩余气泡
        for i in range(1, n):
            # 计算当前气泡的角度位置
            angle = (i - 1) * angle_step
            
            # 计算距离中心的半径（考虑气泡大小）
            # 较大的气泡放置在内环，较小的放置在外环
            bubble_size_factor = (radii[i] - min(radii[1:])) / (max(radii[1:]) - min(radii[1:]) + 0.001)
            distance_from_center = ring_inner_radius + (ring_outer_radius - ring_inner_radius) * (1 - bubble_size_factor)
            
            # 计算位置
            x = distance_from_center * np.cos(angle)
            y = distance_from_center * np.sin(angle)
            
            # 存储位置
            positions[i] = [x, y]
    
    # 应用力导向算法微调位置，避免重叠
    positions = force_directed_adjustment(positions, radii, iterations=50)
    
    return positions

# 力导向算法微调位置，避免气泡重叠
def force_directed_adjustment(initial_positions, radii, iterations=50, repulsion=0.1, attraction=0.2):
    positions = initial_positions.copy()
    n = len(radii)
    
    for _ in range(iterations):
        # 计算每个气泡受到的力
        forces = np.zeros_like(positions)
        
        # 计算气泡之间的排斥力（避免重叠）
        for i in range(n):
            for j in range(n):
                if i != j:
                    # 计算两个气泡之间的向量
                    dx = positions[i, 0] - positions[j, 0]
                    dy = positions[i, 1] - positions[j, 1]
                    distance = max(0.1, np.sqrt(dx**2 + dy**2))
                    
                    # 计算两个气泡应该保持的最小距离（两个半径之和）
                    min_distance = radii[i] + radii[j]
                    
                    # 如果距离小于最小距离，施加排斥力
                    if distance < min_distance:
                        # 排斥力与重叠程度成正比
                        force_magnitude = repulsion * (min_distance - distance) / min_distance
                        
                        # 计算力的方向（单位向量）
                        if distance > 0:
                            force_x = dx / distance * force_magnitude
                            force_y = dy / distance * force_magnitude
                            
                            # 应用力
                            forces[i, 0] += force_x
                            forces[i, 1] += force_y
        
        # 对于非中心气泡，添加向中心的吸引力
        for i in range(1, n):
            # 计算到中心的向量
            dx = positions[i, 0] - positions[0, 0]
            dy = positions[i, 1] - positions[0, 1]
            distance = max(0.1, np.sqrt(dx**2 + dy**2))
            
            # 计算最小安全距离（避免与中心气泡重叠）
            min_safe_distance = radii[0] + radii[i]
            
            # 如果距离大于最小安全距离，施加向中心的吸引力
            if distance > min_safe_distance:
                # 吸引力与距离成正比，但有上限
                force_magnitude = min(attraction * (distance - min_safe_distance) / distance, 0.1)
                
                # 计算力的方向（单位向量，指向中心）
                force_x = -dx / distance * force_magnitude
                force_y = -dy / distance * force_magnitude
                
                # 应用力
                forces[i, 0] += force_x
                forces[i, 1] += force_y
        
        # 更新位置
        positions += forces
    
    return positions

# 计算气泡位置
positions = improved_layout(radii)
x, y = positions[:, 0], positions[:, 1]

# 创建气泡图
plt.figure(figsize=(16, 14))  # 增大图表尺寸以适应更大的字体

# 绘制气泡图
for i, (country, cn_country, weight, color, font_size, radius) in enumerate(zip(
    country_weights[country_column], 
    country_weights['国家'], 
    country_weights[weight_column],
    country_weights['color'],
    country_weights['font_size'],
    country_weights['radius']
)):
    # 绘制气泡
    circle = plt.Circle((x[i], y[i]), radius, color=color, alpha=0.7)
    plt.gca().add_patch(circle)
    
    # 添加国家标签
    plt.annotate(f"{cn_country}\n{weight:.2%}", 
                 (x[i], y[i]),
                 ha='center', va='center',
                 fontsize=font_size)

# 设置图表标题和样式
plt.title('STOXX 国家权重分布', fontsize=36)  # 原来是18，增大两倍
plt.axis('equal')  # 确保圆形不变形

# 移除坐标轴刻度和标签
plt.xticks([])
plt.yticks([])
plt.axis('off')

# 添加图例
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                             label=label, markerfacecolor=color_map[label], markersize=16)  # 原来是10，增大
                  for label in weight_labels]
plt.legend(handles=legend_elements, title="权重区间", loc='lower right', fontsize=16, title_fontsize=20)  # 增大图例字体

# 保存图表
plt.tight_layout()
bubble_chart_path = 'STOXX_country_bubble_chart.png'
plt.savefig(bubble_chart_path, dpi=300, bbox_inches='tight')
plt.show()

# 导出为Excel
output_file_path = 'STOXX_geo_country_weights.xlsx'
country_weights.to_excel(output_file_path, index=False)

# 将气泡图保存到Excel中
wb = Workbook()
ws = wb.active
ws.title = "Country Weights"

# 插入数据
for r in dataframe_to_rows(country_weights, index=False, header=True):
    ws.append(r)

# 插入气泡图
img = Image(bubble_chart_path)
ws.add_image(img, 'D2')

# 保存Excel文件
wb.save(output_file_path)

print(f"已生成国家权重气泡图并保存为 {bubble_chart_path}")
print(f"数据和图表已保存到Excel文件 {output_file_path}")
