import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts

# df = pd.read_csv(r'D:\数据集\covid_data.csv')
# df = pd.read_csv(r'D:\桌面\analysis-of-covid-19-in-asia-master\coronavirus_data.csv')
df = pd.read_csv(r'D:\桌面\analysis-of-covid-19-in-asia-master\covid_data.csv')

#print(df.isnull().sum())

df.isnull().sum()
df = df.dropna(axis=0)

df_m = df.groupby('Country/Other')['Total Cases'].sum().reset_index()
data = [(row['Country/Other'],row['Total Cases']) for idx,row in df_m.iterrows()]

map = Map(
    init_opts = opts.InitOpts(
            theme='dark'
    )
).add(
    "",
    data,
    maptype='world',
    is_map_symbol_show=False,
    label_opts=opts.LabelOpts(is_show=False)
).set_global_opts(
    visualmap_opts=opts.VisualMapOpts(
        max_=df_m["Total Cases"].max(),
        is_piecewise=True,
        pieces=[
            {'min': 500000},
            {'min': 400000, 'max': 500000},
            {'min': 300000, 'max': 400000},
            {'min': 200000, 'max': 300000},
            {'min': 100000, 'max': 200000},
            {'min': 50000, 'max': 100000},
            {'max': 50000}
        ],
        pos_left='5%',
        pos_right='10%',
    ),
    tooltip_opts=opts.TooltipOpts(is_show=True,formatter='{b}:{c}人'),
    legend_opts=opts.LegendOpts(is_show=False),
    title_opts=opts.TitleOpts(
        title="亚洲国家最新 Covid-19 新冠疫情数据",
        pos_top="1%",
        pos_left="center",
        title_textstyle_opts=opts.TextStyleOpts(
            font_family="宋体",
            font_size="20"
        )
    )
)

map.render(path="test_map.html")

