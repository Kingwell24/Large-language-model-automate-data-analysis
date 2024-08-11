# import os
# from langchain_openai import AzureChatOpenAI
# import mysql.connector

# # 设置环境变量
# os.environ["AZURE_OPENAI_API_KEY"] = "e06b809982f3483fa42cc907daf923df"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"

# # 初始化 GPT 接口
# llm = AzureChatOpenAI(
#     azure_deployment="https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
#     api_version="2023-03-15-preview",
#     temperature=0,
#     max_tokens=150,
#     timeout=None,
#     max_retries=2,
# )

# # 连接到 MySQL 数据库
# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Wzx20071201",
#         database="northwind"
#     )

# def get_table_structure():
#     db_connection = get_db_connection()
#     cursor = db_connection.cursor()
#     cursor.execute("SHOW TABLES")
#     tables = cursor.fetchall()
#     table_structure = {}

#     for table in tables:
#         table_name = table[0]
#         cursor.execute(f"DESCRIBE `{table_name}`")
#         columns = cursor.fetchall()
#         column_names = [column[0] for column in columns]
#         table_structure[table_name] = column_names

#     cursor.close()
#     db_connection.close()

#     return table_structure

# def query_database(query):
#     db_connection = get_db_connection()
#     cursor = db_connection.cursor()
#     cursor.execute(query)
#     results = cursor.fetchall()
#     cursor.close()
#     db_connection.close()
#     return results

# def get_sql_query_from_natural_language(natural_language_query, table_structure):
#     structure_info = "The database has the following tables and columns:\n"
#     for table, columns in table_structure.items():
#         structure_info += f"Table `{table}`: Columns {', '.join([f'`{col}`' for col in columns])}\n"

#     messages = [
#         ("system", f"You are a highly skilled SQL query generator. Your task is to convert natural language instructions into accurate SQL queries. Only return the SQL code without any additional text.\n{structure_info}"),
#         ("human", natural_language_query),
#     ]
#     response = llm.invoke(messages)

#     sql_query = response.content.strip()
#     sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

#     for table in table_structure.keys():
#         if " " in table:
#             sql_query = sql_query.replace(f'"{table}"', f'`{table}`')

#     return sql_query

# def get_analysis_from_data(data_str, follow_up_query):
#     messages = [
#         ("system", f"You are a highly skilled data analyst. Your task is to analyze the provided data and respond to further queries based on this data. Here is the data:\n{data_str}"),
#         ("human", follow_up_query),
#     ]
#     response = llm.invoke(messages)
#     return response.content.strip()


import os
from langchain_openai import AzureChatOpenAI
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
from flask import url_for

# 设置环境变量
os.environ["AZURE_OPENAI_API_KEY"] = "e06b809982f3483fa42cc907daf923df"
os.environ[
    "AZURE_OPENAI_ENDPOINT"] = "https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"

# 数据库配置
db_config = {
    'northwind': {
        'host': "localhost",
        'user': "root",
        'password': "Wzx20071201",
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
def get_db_connection(database):
    if database == "northwind":
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wzx20071201",
            database="northwind")
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wzx20071201",
            database="weather_forecast"

    )

def get_table_structure(databse):
    db_connection = get_db_connection(databse)
    cursor = db_connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_structure = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        table_structure[table_name] = column_names

    cursor.close()
    db_connection.close()

    return table_structure

def query_database(query, database):
    db_connection = get_db_connection(database)
    cursor = db_connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
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


def generate_plot(data, plot_type):
    data_description = f"Data: {data.to_dict(orient='list')}"

    # 调用 OpenAI API 生成代码
    response = llm.invoke([
        ("system",
         f"You are a skilled Python developer capable of generating visualization code. Besides the python code don't reply anything to me! Given the data: {data_description}, only generate Python code to create a {plot_type}."),
        ("human", f"Generate Python code to create a {plot_type} plot with the given data."),
    ])

    # 获取生成的代码
    python_code = response.content.strip()
    
    # 去除 Markdown 代码块标记
    python_code = python_code.replace("```python", "").replace("```", "").strip()
    
    # 打印生成的代码用于调试
    print("Generated Python Code:\n", python_code)

    # 创建图像并保存到文件
    try:
        # 创建一个 BytesIO 对象作为图像缓存
        buf = BytesIO()

        # 将数据传递给执行环境
        local_vars = {'plt': plt, 'data': data}
        
        # 执行生成的代码
        exec(python_code, {'plt': plt, 'data': data}, local_vars)
        
        # 生成图像
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()


        
        # 生成图像文件的 URL
        img_url = url_for('static', filename='plot.png')
        return img_url
    except Exception as e:
        print("Error executing generated code:", e)
        return f"Error: {e}"


def get_analysis_from_data(data_str, follow_up_query):
    messages = [
        ("system", f"You are a highly skilled data analyst. Your task is to analyze the provided data and respond to further queries based on this data. Here is the data:\n{data_str}"),
        ("human", follow_up_query),
    ]
    response = llm.invoke(messages)
    return response.content.strip()

    