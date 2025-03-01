import pandas as pd  # 导入pandas库并简写为pd
import matplotlib.pyplot as plt  # 导入matplotlib.pyplot模块并简写为plt
# 自定义一个包含多列数据的数据框DataFrame，包含类别和多列值
data = pd.DataFrame({'category': ["A", "B", "C", "D", "E"],
                    'value1': [10, 15, 7, 12, 8], 'value2': [6, 9, 5, 8, 4],                     
                    'value3': [3, 5, 2, 4, 6], 'value4': [9, 6, 8, 3, 5]})
# 查看数据框
print("Data Structure：")
print(data) 

# 创建堆叠柱状图
data.plot(x='category', kind='bar', stacked=True, figsize=(6, 4))
# 使用DataFrame的plot方法绘制堆叠柱状图# 指定x轴为'category'列，图表类型为'bar'，堆叠为True，图形大小为(6,4)
plt.xlabel('Category')  # 设置x轴标签
plt.ylabel('Value')  # 设置y轴标签
plt.title('Stacked Bar Chart')  # 设置图表标题
plt.xticks(rotation=90)  # 将x轴文字旋转90度，使其垂直显示
plt.legend(title='Values', loc='center', bbox_to_anchor=(1, 0.5))  # 添加图例，并设置标题为'Values'
plt.show()