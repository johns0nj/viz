import pandas as pd # 导入pandas库并简写为pd
import matplotlib.pyplot as plt  # 导入matplotlib.pyplot模块并简写为plt
import seaborn as sns  # 导入seaborn库并简写为sns
# 创建创建一个包含类别、值和标准差的DataFrame数据集
data = pd.DataFrame({'category': ["A", "B", "C", "D", "E"],                     
                     'value': [10, 15, 7, 12, 8], 'std': [1, 2, 1.5, 1.2, 2.5]})
# 计算每个类别的均值和标准差
mean_values = data['value']
std_values = data['std']
colors = sns.color_palette("Set1", n_colors=len(data))  # 创建颜色调色板# 创建均值柱状图
plt.figure(figsize=(6, 4))  # 创建图形对象，并设置图形大小
bars = plt.bar(data['category'], mean_values, color=colors)# 绘制柱状图，指定x轴为类别，y轴为均值，柱状颜色为颜色调色板中的颜色
# 添加误差线
for i, (bar, std) in enumerate(zip(bars, std_values)):    
    plt.errorbar(bar.get_x() + bar.get_width() / 2, bar.get_height(),                 
                 # 在柱状图的中心位置添加误差线                 
                yerr=std, fmt='none', color='black', ecolor='gray',                 # 设置误差线的样式和颜色
                capsize=5, capthick=2)  # 设置误差线的帽子大小和线宽# 添加标题和标签
plt.xlabel('Category')  # 设置x轴标签
plt.ylabel('Mean Value')  # 设置y轴标签
plt.title('Mean Bar Chart with Error Bars')  # 设置图表标题
# 设置网格线的样式、颜色和透明度
plt.grid(axis='both', linestyle='-', color='gray', alpha=0.5)
plt.show()