from collections import namedtuple
import pandas as pd
import numpy as np
import copy
import sys

Vrange = namedtuple("Vrange", ["lo", "hi"])
ColIndex = namedtuple("ColIndex", ["icol", "col_name"])

od = pd.read_csv(sys.argv[1], encoding="gb18030")
titles = od.columns
od1 = od[(od[titles[0]]==55593)]
od2 = od[(od[titles[0]]==57584)]
raw_data = copy.deepcopy(od1)


indexs_all = dict(
temperature_indexs = {i: col for i, col in enumerate(titles) if "温" in col},
air_pressure_indexs = {i: col for i, col in enumerate(titles) if "气压" in col},
wate_pressure_indexs = {i: col for i, col in enumerate(titles) if "水汽压" in col},
relative_indexs = {i: col for i, col in enumerate(titles) if "相对" in col},
rain_indexs = {i: col for i, col in enumerate(titles) if "降水量" in col},
wind_ve_indexs = {i: col for i, col in enumerate(titles) if "风速" in col and "风向" not in col},
wind_dir_indexs = {i: col for i, col in enumerate(titles) if "风向" in col},
day_hours_indexs = {i: col for i, col in enumerate(titles) if "时数" in col},
vaper_indexs = {i: col for i, col in enumerate(titles) if "蒸发量" in col},
)
icol_indexs = dict()
for name, _map in indexs_all.items():
    icol_indexs.update({key: name for key in _map.keys()})

indexs_range = dict(
temperature_indexs = Vrange(-100, 100),
air_pressure_indexs = Vrange(0, 2000),
wate_pressure_indexs = Vrange(0, 100),
relative_indexs = Vrange(0, 100),
rain_indexs = Vrange(0, 1000),
wind_ve_indexs = Vrange(0, 100),
wind_dir_indexs = Vrange(1, 16),
day_hours_indexs = Vrange(0, 24),
vaper_indexs = Vrange(0, 1000),
)

def is_col_value_in_range(icol, df):
    col = df[titles[icol]]
    desc = col.describe()
    vrange = indexs_range[icol_indexs[icol]]
    if vrange.lo <= desc["min"] and desc["max"] <= vrange.hi:
        return True
    else:
        False

def value_change(x):
    if 32000 <= x < 33000:
        return (x - 32000) * 0.1
    elif 31000 <= x < 32000:
        return (x - 31000) * 0.1
    elif 30000 <= x < 31000:
        return (x - 30000) * 0.1
    
def check_data_valid(df):
    passes = []
    faileds = []
    for _, d in indexs_all.items():
        for i, col_name in d.items():
            if is_col_value_in_range(i, df):
                passes.append(ColIndex(i, col_name))
            else:
                faileds.append(ColIndex(i, col_name))
    return passes, faileds

def replace_invalid_by_nan(od):
    for icol in range(4,len(titles)):
        title = titles[icol]
        col = od[title]
        new = col.replace([32744, 32766], np.nan)
        new = new.replace(32700, 0)
        od.loc[:, title] = new
    return od


p, f = check_data_valid(od1)
print(f)
replace_invalid_by_nan(od1)
p, f = check_data_valid(od1)
print(f)
