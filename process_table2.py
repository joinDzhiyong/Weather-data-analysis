import sys
from prepare_data import PreResolver
import pandas as pd


class ProcesserTable2:
    def __init__(self, df: pd.DataFrame) -> None:
        self.data = df
        self.cols = self.data.columns

    def get_max_value_coresp_value(self, i, j): #i max value, j corespond value
        directions = []
        max_mon = self.data.groupby([self.cols[1], self.cols[2]]).max()
        a = max_mon.loc[:, self.cols[i]]
        for year, mon in a.index:
            v = a.loc[year, mon]
            _raws = self.data[(self.data.loc[:, self.cols[i]] == v) & (self.data.loc[:, self.cols[1]] == year) & (self.data.loc[:, self.cols[2]] == mon)]
            array = _raws.pop(self.cols[j]).values
            directions.append((year, mon, array))
        return directions

    def get_table2_mon_df(self):
        mean_mon = self.data.groupby([self.cols[1], self.cols[2]]).mean()
        max_mon = self.data.groupby([self.cols[1], self.cols[2]]).max()
        min_mon = self.data.groupby([self.cols[1], self.cols[2]]).min()
        sum_mon = self.data.groupby([self.cols[1], self.cols[2]]).sum()
        res = {
        "平均气温": mean_mon.loc[:, self.cols[4]],
        "平均最高气温": mean_mon.loc[:, self.cols[5]],
        "平均最低气温": mean_mon.loc[:, self.cols[6]],
        "最高气温": max_mon.loc[:, self.cols[5]],
        "最低气温": min_mon.loc[:, self.cols[6]],
        "降水量": sum_mon.loc[:, self.cols[14]],
        "日照和": sum_mon.loc[:, self.cols[20]],
        "蒸发和(小型)": sum_mon.loc[:, self.cols[-3]],
        "蒸发和（大型）": sum_mon.loc[:, self.cols[-2]],
        "平均地表气温": mean_mon.loc[:, self.cols[21]],
        "平均地表最高气温": mean_mon.loc[:, self.cols[22]],
        "平均地表最低气温": mean_mon.loc[:, self.cols[23]],
        "地表最高气温": max_mon.loc[:, self.cols[22]],
        "地表最低气温": max_mon.loc[:, self.cols[23]],
        "平均风速": mean_mon.loc[:, self.cols[15]],
        "最大风速": max_mon.loc[:, self.cols[16]],
        "极大风速": max_mon.loc[:, self.cols[18]],
        }
        res1 = {
            "最大风速对应风向": self.get_max_value_coresp_value(16, 17),
            "极大风速对应风向": self.get_max_value_coresp_value(18, 19)
        }
        t = pd.DataFrame.from_dict(res)
        t1 = pd.DataFrame.from_records(res1["最大风速对应风向"], columns=["年", "月", "最大风速对应风向"])
        t2 = pd.DataFrame.from_records(res1["极大风速对应风向"], columns=["年", "月", "极大风速对应风向"])
        t3 = pd.merge(t1, t2)
        t4 = pd.merge(t, t3, left_index=True, right_on=["年", "月"])
        year_col = t4.pop("年")
        t4.insert(0, year_col.name, year_col)
        mon_col = t4.pop("月")
        t4.insert(0, mon_col.name, mon_col)
        return t4

    def to_csv(self, df, to, encoding="gb18030"):
        df.to_csv(to, encoding=encoding, index=False)