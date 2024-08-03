import os
from langchain_openai import AzureChatOpenAI
import mysql.connector

# 设置环境变量
os.environ["AZURE_OPENAI_API_KEY"] = "e06b809982f3483fa42cc907daf923df"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"

# 连接到 MySQL 数据库
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="52zz468275",
    database="northwind"
)
cursor = db_connection.cursor()

# 初始化 GPT 接口
llm = AzureChatOpenAI(
    azure_deployment="https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
    api_version="2023-03-15-preview",
    temperature=0,
    max_tokens=150,
    timeout=None,
    max_retries=2,
)

# 首先让GPT读取传入的数据库信息，包括表头列名，方便后续查询
def get_table_structure():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_structure = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        table_structure[table_name] = column_names

    return table_structure

# 将转换好的SQL查询语句在MySQL中运行
def query_database(query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# 处理自然语言生成的结果
def get_sql_query_from_natural_language(natural_language_query, table_structure):
    structure_info = "The database has the following tables and columns:\n"
    for table, columns in table_structure.items():
        structure_info += f"Table {table}: Columns {', '.join(columns)}\n"

    messages = [
        ("system", f"You are a highly skilled SQL query generator. Your task is to convert natural language instructions into accurate SQL queries. Only return the SQL code without any additional text.\n{structure_info}"),
        ("human", natural_language_query),
    ]
    response = llm.invoke(messages)

    sql_query = response.content.strip()
    # 去除 SQL 查询中的 Markdown 代码块标记
    sql_query = sql_query.replace("sql", "").replace("", "").strip()
    return sql_query

# 获取数据库结构
table_structure = get_table_structure()
print("Database Structure:", table_structure)

# 示例自然语言查询
natural_language_query = "查询每个客户的公司名称"

# 将自然语言查询转换为 SQL 查询
sql_query = get_sql_query_from_natural_language(natural_language_query, table_structure)
print("Generated SQL Query:", sql_query)

# 执行 SQL 查询
try:
    results = query_database(sql_query)
    print("Query Results:", results)
except mysql.connector.Error as err:
    print("Error: {}".format(err))


# 关闭数据库连接
cursor.close()
db_connection.close()