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
from flask import url_for, request
import time
import datetime
import time

# 设置环境变量
os.environ["AZURE_OPENAI_API_KEY"] = "e06b809982f3483fa42cc907daf923df"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"

# 数据库配置
db_config = {
    'Database_1': {
        'host': "localhost",
        'user': "root",
        'password': "52zz468275",
        'database': "northwind"
    },
    'Database_2': {
        'host': "localhost",
        'user': "root",
        'password': "52zz468275",
        'database': "co2"
    },
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

# 连接到 MySQL 数据库 (用户自行修改为本地数据库)
def get_db_connection(database):
    if database == "Database_1":
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="52zz468275",
            database="northwind")
    elif database == "Database_2":
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="52zz468275",
            database="co2")

def get_table_structure(database):
    db_connection = get_db_connection(database)
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
def get_sql_query_from_natural_language(natural_language_query, table_structure, chat_history):
    structure_info = "The database has the following tables and columns:\n"
    for table, columns in table_structure.items():
        structure_info += f"Table `{table}`: Columns {', '.join([f'`{col}`' for col in columns])}\n"

    # Include chat history in the context
    messages = [
        ("system", f"You are a highly skilled SQL query generator. Your task is to convert natural language instructions into accurate SQL queries. Only return the SQL code without any additional text.\n{structure_info}"),
    ] + chat_history + [("human", natural_language_query)]

    response = llm.invoke(messages)

    sql_query = response.content.strip()
    # 去除 SQL 查询中的 Markdown 代码块标记
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    print(sql_query)

    # 特殊处理表名中的空格
    for table in table_structure.keys():
        if " " in table:
            sql_query = sql_query.replace(table, f'`{table}`')

    return sql_query



def generate_plot(instructions, chat_history_str, plot_type):
    """
    Generates a plot based on the chat history and specified plot type.
    
    :param instructions: Instructions provided by the user for further customization
    :param chat_history_str: Context provided for generating the plot code
    :param plot_type: Type of plot to be generated (e.g., 'bar', 'line', 'pie', 'scatter')
    :return: URL of the generated plot image or an error message
    """
    # Call OpenAI API to generate code
    try:
        response = llm.invoke([
            ("system",
             f"You are a skilled Python developer capable of generating visualization code. Besides the python code don't reply anything to me! Given the following data:\n{chat_history_str}, and the following instructions:\n{instructions}, only generate Python code to create a {plot_type}."),
            ("human", f"Generate Python code to create a {plot_type} plot with the given context."),
        ])
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error: {e}"

    # Get generated code
    python_code = response.content.strip()

    # Clean up the generated code
    python_code = python_code.replace("```python", "").replace("```", "").strip()

    # Debug logging
    print("Generated Python Code:\n", python_code)

    # Create plot and save to file
    try:
        buf = BytesIO()

        # Execute the generated code
        exec(python_code, globals())

        # Save the plot to the buffer
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Generate image filename and path
        img_filename = f"plot_{request.remote_addr}_{os.getpid()}_{int(time.time())}.png"
        img_path = os.path.join('static', 'images', img_filename)

        # Save the image to file
        with open(img_path, 'wb') as f:
            f.write(buf.getbuffer())

        # Return the URL of the generated plot image
        return url_for('static', filename=f'images/{img_filename}')

    except Exception as e:
        print(f"Error executing plot code: {e}")
        return f"Error: {e}"





def get_analysis_from_data(data_str, follow_up_query):
    messages = [
        ("system", f"You are a highly skilled data analyst. Your task is to analyze the provided data and respond to further queries based on this data. Here is the data:\n{data_str}"),
        ("human", follow_up_query),
    ]
    response = llm.invoke(messages)
    return response.content.strip()

    