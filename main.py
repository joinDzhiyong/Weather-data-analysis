import pandas as pd

od = pd.read_csv("origin_data.csv", encoding="gb18030")
cols = od.columns
od1 = od[(od[cols[0]]==55593)]
od2 = od[(od[cols[0]]==57584)]

mean = od1.mean()
for col in cols:
    if "平均" in col:
        print("{}:{}".format(col, mean[col]))