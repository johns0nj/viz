import pandas as pd
import numpy as np
from dash import Dash, dash_table, html
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from dash.dependencies import Input, Output
import io

# 读取数据
file_path = 'STOXX.csv'
data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

# 计算每日收益率
returns = data.pct_change().dropna()

# 计算年化收益率
annual_returns = returns.mean() * 252

# 计算年化波动率
annual_volatility = returns.std() * np.sqrt(252)

# 假设无风险利率为0.02（2%）
risk_free_rate = 0.02

# 计算Sharpe Ratio
sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility

# 创建结果表格
df_results = pd.DataFrame({
    '指数': ['STOXX 600', 'STOXX 50', 'STOXX Mid 200'],
    '年化收益率': annual_returns,
    '年化波动率': annual_volatility,
    'Sharpe Ratio': sharpe_ratio
})

# 格式化为百分数
df_results['年化收益率'] = df_results['年化收益率'].apply(lambda x: f'{x:.2%}')
df_results['年化波动率'] = df_results['年化波动率'].apply(lambda x: f'{x:.2%}')

# 创建柱状图
fig, ax = plt.subplots(figsize=(8, 6))
colors = sns.color_palette("Set1", n_colors=len(df_results))
bars = ax.bar(df_results['指数'], annual_returns, yerr=annual_volatility, color=colors, capsize=5)
ax.set_title('年化收益率和标准差', fontproperties='SimHei')
ax.set_ylabel('年化收益率', fontproperties='SimHei')
ax.set_xlabel('指数', fontproperties='SimHei')

# 设置Sharpe Ratio保留两位小数
df_results['Sharpe Ratio'] = df_results['Sharpe Ratio'].apply(lambda x: round(x, 2))

# 将图表保存为图像
buf = BytesIO()
plt.savefig(buf, format="png")
data = base64.b64encode(buf.getbuffer()).decode("utf8")

# 创建Dash应用程序
app = Dash(__name__)

app.layout = html.Div([
    html.H1("STOXX 指数分析结果"),
    dash_table.DataTable(
        id='results-table',
        columns=[{"name": "指数", "id": "指数"}] + [{"name": i, "id": i} for i in df_results.columns if i != '指数'],
        data=df_results.to_dict('records'),
        style_table={'width': '50%'},
        style_cell={'textAlign': 'center'},
        export_format='xlsx',  # 支持导出为Excel
    ),
    html.Button("导出为Excel", id="export-button"),
    html.Img(src="data:image/png;base64,{}".format(data))
])

# 添加回调函数处理导出
@app.callback(
    Output('results-table', 'export_headers'),
    [Input('export-button', 'n_clicks')]
)
def export_to_excel(n_clicks):
    if n_clicks:
        # 将DataFrame转换为Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_results.to_excel(writer, index=False)
        output.seek(0)
        return {'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'Content-Disposition': 'attachment; filename=STOXX_Results.xlsx'}
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
