import matplotlib.pyplot as plt
import numpy as np

# 示例数据
categories = ['A', 'B', 'C', 'D']
values = [10, 15, 7, 12]
errors = [1, 2, 1.5, 0.8]  # 误差值（可以是标准差、标准误差等）

# 绘制带误差棒的柱状图
plt.bar(categories, values, yerr=errors, capsize=5, color='skyblue', edgecolor='black')

# 添加标签和标题
plt.xlabel('Category')
plt.ylabel('Value')
plt.title('Bar Chart with Error Bars')

# 显示图表
plt.show() 