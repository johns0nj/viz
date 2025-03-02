import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 创建图形和轴对象
fig, ax = plt.subplots(figsize=(15, 10))

# 定义颜色
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF']

# ETF类型及其特点
etf_types = {
    '全市场ETF': {
        '特点': ['覆盖整个欧洲市场', '包含大中小盘股', '行业分布广泛'],
        '适合投资者': ['希望全面覆盖市场', '寻求市场整体表现', '风险承受力中等']
    },
    '大盘股ETF': {
        '特点': ['投资大型公司', '波动性较低', '稳定性高'],
        '适合投资者': ['偏好蓝筹股', '寻求稳定收益', '风险承受力较低']
    },
    '中盘股ETF': {
        '特点': ['投资中型公司', '成长性较好', '波动性较高'],
        '适合投资者': ['追求较高收益', '接受较高波动', '风险承受力较高']
    },
    '小盘股ETF': {
        '特点': ['投资小型公司', '高成长潜力', '波动性最高'],
        '适合投资者': ['追求高收益', '接受高波动', '风险承受力最高']
    },
    '区域ETF': {
        '特点': ['特定区域投资', '区域集中度高', '受区域因素影响'],
        '适合投资者': ['看好特定区域', '区域配置需求', '风险承受力中等']
    },
    'ESG ETF': {
        '特点': ['符合ESG标准', '可持续发展', '社会责任投资'],
        '适合投资者': ['关注可持续发展', '重视社会责任', '风险承受力中等']
    }
}

# 设置y轴位置
y_positions = np.arange(len(etf_types)) * 2

# 绘制ETF类型和信息
for i, (etf_type, info) in enumerate(etf_types.items()):
    # ETF类型
    ax.text(-0.1, y_positions[i], etf_type, fontsize=12, fontweight='bold')
    
    # 特点
    rect1 = patches.Rectangle((0.2, y_positions[i]-0.3), 0.25, 0.6, 
                            facecolor=colors[i], alpha=0.3)
    ax.add_patch(rect1)
    features = '\n'.join(info['特点'])
    ax.text(0.3, y_positions[i], features, fontsize=10, va='center')
    
    # 适合投资者
    rect2 = patches.Rectangle((0.6, y_positions[i]-0.3), 0.25, 0.6, 
                            facecolor=colors[i], alpha=0.3)
    ax.add_patch(rect2)
    investors = '\n'.join(info['适合投资者'])
    ax.text(0.7, y_positions[i], investors, fontsize=10, va='center')

# 设置标题和标签
plt.title('欧洲宽基指数ETF分类及特点', fontsize=14, pad=20)
ax.text(0.3, max(y_positions) + 1, '主要特点', fontsize=12, fontweight='bold')
ax.text(0.7, max(y_positions) + 1, '适合投资者', fontsize=12, fontweight='bold')

# 设置轴的范围和隐藏轴线
ax.set_xlim(-0.2, 1)
ax.set_ylim(min(y_positions)-1, max(y_positions)+1.5)
ax.axis('off')

plt.tight_layout()
plt.show()
