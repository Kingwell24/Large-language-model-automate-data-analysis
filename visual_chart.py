import os
from langchain_openai import AzureChatOpenAI
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置环境变量
os.environ["AZURE_OPENAI_API_KEY"] = "e06b809982f3483fa42cc907daf923df"
os.environ[
    "AZURE_OPENAI_ENDPOINT"] = "https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"

# 数据库配置
db_config = {
    'northwind': {
        'host': "localhost",
        'user': "root",
        'password': "52zz468275",
        'database': "northwind"
    },
    'weather_forecast': {
        'host': "localhost",
        'user': "root",
        'password': "52zz468275",
        'database': "weather_forecast"
    }
}

# 初始化 GPT 接口
llm = AzureChatOpenAI(
    azure_deployment="https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
    api_version="2023-03-15-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 连接到 MySQL 数据库
def connect_to_database(db_choice):
    config = db_config[db_choice]
    return mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

# 首先让GPT读取传入的数据库信息，包括表头列名，方便后续查询
def get_table_structure(cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_structure = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        table_structure[table_name] = column_names

    return table_structure

# 将转换好的SQL查询语句在MySQL中运行
def query_database(cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# 处理自然语言生成的结果
def get_sql_query_from_natural_language(natural_language_query, table_structure):
    structure_info = "The database has the following tables and columns:\n"
    for table, columns in table_structure.items():
        structure_info += f"Table `{table}`: Columns {', '.join([f'`{col}`' for col in columns])}\n"

    messages = [
        ("system",
         f"You are a highly skilled SQL query generator. Your task is to convert natural language instructions into accurate SQL queries. Only return the SQL code without any additional text.\n{structure_info}"),
        ("human", natural_language_query),
    ]
    response = llm.invoke(messages)

    sql_query = response.content.strip()
    # 去除 SQL 查询中的 Markdown 代码块标记
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # 特殊处理表名中的空格
    for table in table_structure.keys():
        if " " in table:
            sql_query = sql_query.replace(table, f'`{table}`')

    return sql_query

# 生成绘图代码的函数
def generate_plot_code(data, plot_type):
    data_description = f"Data: {data.to_dict(orient='list')}"

    # 调用 OpenAI API 生成代码
    response = llm.invoke([
        ("system",
         f"You are a skilled Python developer capable of generating visualization code. Besides the python code don't reply anything to me! Given the data: {data_description}, only generate Python code to create a {plot_type}."),
        ("human", f"Generate Python code to create a {plot_type} plot with the given data."),
    ])

    return response.content.strip()

# 选择数据库
db_choice = input("请选择要查询的数据库 (northwind/weather_forecast): ").strip()
db_connection = connect_to_database(db_choice)
cursor = db_connection.cursor()

# 获取数据库结构
table_structure = get_table_structure(cursor)
print("Database Structure:", table_structure)

# 第一次自然语言查询
natural_language_query = input("请输入自然语言查询：")
sql_query = get_sql_query_from_natural_language(natural_language_query, table_structure)
print("Generated SQL Query:", sql_query)

# 执行 SQL 查询
try:
    results = query_database(cursor, sql_query)
    print("Query Results:", results)
except mysql.connector.Error as err:
    print("Error: {}".format(err))
    results = []

# 将查询结果转换为 DataFrame 以便于生成图表
if results:
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)

    # 进一步详细分析
    while True:
        follow_up_query = input("请输入进一步的详细分析请求（输入'退出'以结束对话）：")
        if follow_up_query.lower() == '退出':
            break

        if "绘制图表" in follow_up_query:
            # 生成绘图代码
            plot_code = generate_plot_code(df, follow_up_query)

            # 打印生成的代码以供调试
            print("Generated Plot Code:")
            plot_code = plot_code.replace("```python", "").replace("```", "").strip()
            print(plot_code)

            # 执行生成的绘图代码
            try:
                exec(plot_code)
            except Exception as e:
                print(f"Error executing plot code: {e}")
        else:
            # 进行数据分析
            messages = [
                ("system", f"You are a highly skilled data analyst. Your task is to analyze the provided data and respond to further queries based on this data. Here is the data:\n{df.to_string()}"),
                ("human", follow_up_query),
            ]
            response = llm.invoke(messages)

            analysis_result = response.content.strip()
            print("Analysis Result:", analysis_result)

# 关闭数据库连接
cursor.close()
db_connection.close()
