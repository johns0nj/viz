import pandas as pd

# 读取数据
file_path = 'EQT_BOND_spd.xlsx'
data = pd.read_excel(file_path)

# 检查列名
print("文件中的列名：", data.columns)

# 将所有空白数据用前一天的数据补齐
data.ffill(inplace=True)

# 计算STOXX 50的SX5E Index - BEst P/E Ratio (L1)列的倒数
if 'SX5E Index - BEst P/E Ratio (L1)' in data.columns:
    data['SX5E Index - BEst P/E Ratio (L1)'] = 1 / data['SX5E Index - BEst P/E Ratio (L1)']
else:
    print("错误：文件中没有 'SX5E Index - BEst P/E Ratio (L1)' 列")

# 保存更新后的数据
output_file_path = 'EQT_BOND_spd_updated.xlsx'
data.to_excel(output_file_path, index=False)
