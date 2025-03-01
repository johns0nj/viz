import pandas as pd  # 导入pandas库并简写为pd
import matplotlib.pyplot as plt  # 导入matplotlib.pyplot模块并简写为plt
# 自定义一个包含多列数据的数据框DataFrame，包含类别和多列值
data = pd.DataFrame({'category': ["A", "B", "C", "D", "E"],
                    'value1': [10, 15, 7, 12, 8], 'value2': [6, 9, 5, 8, 4],                     
                    'value3': [3, 5, 2, 4, 6], 'value4': [9, 6, 8, 3, 5]})
# 查看数据框
print("Data Structure：")
print(data) 

data_percentage = data.copy()
# 计算每个数值列的百分比，除以每行的总和并乘以100
data_percentage.iloc[:, 1:] = data_percentage.iloc[:, 1:].div(    data_percentage.iloc[:, 1:].sum(axis=1), axis=0) * 100
data_percentage.set_index('category').plot(kind='bar',                                           stacked=True, figsize=(6, 4))

# 创建百分比堆叠柱状图，设置索引为'category'列，# 图表类型为'bar'，堆积模式为True，图形大小为(6,4)
plt.xlabel('Category')  # 设置x轴标签
plt.ylabel('Percentage')  # 设置y轴标签
plt.title('Percentage Stacked Bar Chart')  # 设置图表标题
plt.xticks(rotation=0)  # 旋转x轴文本，使其水平显示
# 添加图例，并设置标题为'Values'，并放置在图的右侧
plt.legend(title='Values', loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()