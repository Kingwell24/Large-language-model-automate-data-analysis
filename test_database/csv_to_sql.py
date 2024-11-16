import pandas as pd
from sqlalchemy import create_engine

# 读取 CSV 文件
df = pd.read_csv(r"owid-co2-data.csv")

# 创建数据库连接
engine = create_engine('mysql+mysqlconnector://root:52zz468275@localhost/CO2')

# 将数据导入到 MySQL 表中
df.to_sql('people', con=engine, if_exists='append', index=False)
