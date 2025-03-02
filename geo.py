import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows

# 读取数据
file_path = 'STOXX_geo.xlsx'
data = pd.read_excel(file_path)
print(data.columns)

# 按INDUSTRY_GROUP计算权重
industry_weights = data.groupby('INDUSTRY_GROUP')['Unnamed: 3'].sum().reset_index()

# 按权重从大到小排序
industry_weights = industry_weights.sort_values(by='Unnamed: 3', ascending=False)

# 只保留前10个，其余归为"Others"
if len(industry_weights) > 10:
    top_10 = industry_weights.head(10)
    others = pd.DataFrame({
        'INDUSTRY_GROUP': ['Others'],
        'Unnamed: 3': [industry_weights['Unnamed: 3'][10:].sum()]
    })
    industry_weights = pd.concat([top_10, others])

# 绘制饼图
plt.figure(figsize=(8, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#d3d3d3']
plt.pie(industry_weights['Unnamed: 3'], labels=industry_weights['INDUSTRY_GROUP'], autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Industry Group Weight Distribution')
plt.show()

# 导出为Excel
output_file_path = 'STOXX_geo_industry_weights.xlsx'
industry_weights.to_excel(output_file_path, index=False)

# 将饼图保存为Excel中的图表
wb = Workbook()
ws = wb.active
ws.title = "Industry Weights"

# 插入数据
for r in dataframe_to_rows(industry_weights, index=False, header=True):
    ws.append(r)

# 插入饼图
pie_chart_path = 'industry_pie_chart.png'
plt.savefig(pie_chart_path, bbox_inches='tight')

# 插入饼图
img = Image(pie_chart_path)
ws.add_image(img, 'D2')

# 保存Excel文件
wb.save(output_file_path)
