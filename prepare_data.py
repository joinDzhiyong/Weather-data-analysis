from collections import namedtuple
import pandas as pd
import numpy as np

Vrange = namedtuple("Vrange", ["lo", "hi"])

od = pd.read_csv("origin_data.csv", encoding="gb18030")
cols = od.columns
od1 = od[(od[cols[0]]==55593)]

# temperature =  od1[cols[4]]
# wrong_value = temperature[(temperature > 100) | (temperature < -100)]
# assert len(wrong_value) == 0
all_indexs = dict(
temperature_indexs = {i: col for i, col in enumerate(cols) if "温" in col},
air_pressure_indexs = {i: col for i, col in enumerate(cols) if "气压" in col},
wate_pressure_indexs = {i: col for i, col in enumerate(cols) if "水汽压" in col},
relative_indexs = {i: col for i, col in enumerate(cols) if "相对" in col},
rain_indexs = {i: col for i, col in enumerate(cols) if "降水量" in col},
wind_ve_indexs = {i: col for i, col in enumerate(cols) if "风速" in col and "风向" not in col},
wind_dir_indexs = {i: col for i, col in enumerate(cols) if "风向" in col},
day_hours_indexs = {i: col for i, col in enumerate(cols) if "时数" in col},
vaper_indexs = {i: col for i, col in enumerate(cols) if "蒸发量" in col},
)

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

