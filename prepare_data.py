from collections import namedtuple
import pandas as pd
import numpy as np
import copy
import sys

Vrange = namedtuple("Vrange", ["lo", "hi"])
ColIndex = namedtuple("ColIndex", ["icol", "col_name"])


class PreResolver:
    def __init__(self, data_file, n) -> None:
        self.raw_data = pd.read_csv(data_file, encoding="gb18030")
        self.data = copy.deepcopy(self.raw_data)
        self.titles = self.raw_data.columns
        self.data = self.data[(self.data.iloc[:, 0]==n)]
        self.get_indexs()

    def value_change(self, x:int):
        if 32000 <= x < 33000:
            return (x - 32000) * 0.1
        elif 31000 <= x < 32000:
            return (x - 31000) * 0.1
        elif 30000 <= x < 31000:
            return (x - 30000) * 0.1
        else:
            return x

    def get_indexs(self):
        self.indexs_all = dict(
        temperature_indexs = {i: col for i, col in enumerate(self.titles) if "温" in col},
        air_pressure_indexs = {i: col for i, col in enumerate(self.titles) if "气压" in col},
        wate_pressure_indexs = {i: col for i, col in enumerate(self.titles) if "水汽压" in col},
        relative_indexs = {i: col for i, col in enumerate(self.titles) if "相对" in col},
        rain_indexs = {i: col for i, col in enumerate(self.titles) if "降水量" in col},
        wind_ve_indexs = {i: col for i, col in enumerate(self.titles) if "风速" in col and "风向" not in col},
        wind_dir_indexs = {i: col for i, col in enumerate(self.titles) if "风向" in col},
        day_hours_indexs = {i: col for i, col in enumerate(self.titles) if "时数" in col},
        vaper_indexs = {i: col for i, col in enumerate(self.titles) if "蒸发量" in col},
        )
        self.icol_indexs = dict()
        for name, _map in self.indexs_all.items():
            self.icol_indexs.update({key: name for key in _map.keys()})

        self.indexs_range = dict(
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


    def is_col_value_in_range(self, i):
        col = self.data.iloc[:, i]
        desc = col.describe()
        vrange = self.indexs_range[self.icol_indexs[i]]
        if vrange.lo <= desc["min"] and desc["max"] <= vrange.hi:
            return True
        else:
            False
    
    def check_data_valid(self):
        passes = []
        faileds = []
        for _, d in self.indexs_all.items():
            for i, col_name in d.items():
                if self.is_col_value_in_range(i):
                    passes.append(ColIndex(i, col_name))
                else:
                    faileds.append(ColIndex(i, col_name))
        return passes, faileds

    def replace_invalid_by_nan(self):
        for i in range(4, self.titles.size):
            col = self.data.iloc[:, i]
            col.replace([32744, 32766], np.nan, inplace=True)
            col.replace(32700, 0, inplace=True)
            new = col.map(self.value_change, 'ignore')
            self.data.iloc[:, i] = new
    
    def process_over_all(self):
        p, f = self.check_data_valid()
        print("before clean:")
        print(p)
        print(f)
        self.replace_invalid_by_nan()
        p, f = self.check_data_valid()
        print("after clean:")
        print(p)
        print(f)


if __name__ == "__main__":
    prsr = PreResolver(sys.argv[1], 55593)
    prsr1 = PreResolver(sys.argv[1], 57584)
    # od1 = od[(od[titles[0]]==55593)]
    # od2 = od[(od[titles[0]]==57584)]
