import sys
import pandas as pd
from prepare_data import PreResolver

pr = PreResolver(sys.argv[1], 55593)
pr.process_over_all()
od1 = pr.data
cols = od1.columns
indexs_table1 = ["类型", "数值", "日期"]
map1_table1 = {
"多年平均年降水量": 14,	
"多年平均最大日降水量": 14,	
"最大一日降水量": 14,
"多年极大风速": -9,	
"最大一日极大风速极值": -9,
"最大一日极大风速风向": -8	
}
map1_table1_mean_mean = {
"多年平均气压": 7,	
"多年平均水汽压": -1,	
"多年平均相对湿度": 10,	
"多年平均气温": 4,	
"多年平均风速": 15,
}       #每日的平均值
map1_table1.update(map1_table1_mean_mean)
mean_by_year_mean =od1.groupby(cols[1]).mean().mean()
res = {}
for key, value in map1_table1_mean_mean.items():
    res[key] = (mean_by_year_mean[cols[value]], None)

res["多年平均年降水量"] = (od1.groupby(cols[1]).sum().mean()[cols[14]], None)
res["多年平均最大日降水量"] = (od1.groupby(cols[1]).max().mean()[cols[14]], None)
shui_max_max = od1.groupby(cols[1]).max().max()[cols[14]]
_raw = od1[od1[cols[14]] == shui_max_max]
date = "{}年{}月{}日".format(_raw[cols[1]], _raw[cols[2]], _raw[cols[3]])
res["最大一日降水量"] = (shui_max_max, date)
res["多年极大风速"] = (od1.groupby(cols[1]).max().mean()[cols[-9]], None)
fensu_max_max = od1.groupby(cols[1]).max().max()[cols[-9]]
_raw = od1[od1[cols[-9]] == fensu_max_max]
date = "{}年{}月{}日".format(_raw[cols[1]], _raw[cols[2]], _raw[cols[3]])
res["最大一日极大风速极值"] = (fensu_max_max, date)
res["最大一日极大风速风向"] = (od1[od1[cols[-9]] == 28.0][cols[-8]], None)