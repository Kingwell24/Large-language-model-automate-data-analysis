from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from lc import llm,get_sql_query_from_natural_language, query_database, get_table_structure, get_analysis_from_data, generate_plot
import pandas as pd
import datetime
from prettytable import PrettyTable
#test
app = Flask(__name__) 

chat_histories = {} # 用于存储聊天记录

app.secret_key = os.urandom(24)  # 生成一个随机的 24 字节的密钥

# 连接到 MySQL 数据库 (用户自行修改为本地数据库)
def get_db_connection(database):
    if database == "northwind":
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="52zz468275",
            database="northwind")
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="52zz468275",
            database="co2"

    )

@app.route('/')
def index():
    return render_template('web_main.html')

@app.route('/main/ask')
def main():
    # if 'username' not in session:
    #     return redirect(url_for('signin'))
    return render_template('web_ask.html')

@app.route('/main/graph_showing')
def graph_showing_page():
    return render_template('graph_showing.html')


@app.route('/get_table_structure', methods=['POST'])
def get_table_structure_route():
    data = request.json
    db_choice = data.get('database')

    if not db_choice:
        return jsonify({'error': 'No database provided'}), 400

    # 获取数据库结构
    table_structure = get_table_structure(db_choice)

    return jsonify({'table_structure': table_structure})

#  获取表结构
@app.route('/table_structure', methods=['POST'])
def table_structure():
    data = request.json
    database = data.get('database')

    if not database:
        return jsonify({'error': 'No database selected'}), 400

    table_structure = get_table_structure(database)
    
    # 格式化表结构信息
    formatted_structure = ""
    for table, columns in table_structure.items():
        formatted_structure += f"<strong>Table `{table}`:</strong><br>Columns: {', '.join([f'`{col}`' for col in columns])}<br><br>"

    return jsonify({'table_structure': formatted_structure})

# 问答
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    db_choice = data.get('database')
    is_sql_query = data.get('is_sql_query', False)
    user_id = data.get('user_id')  # 添加 user_id 以区分不同用户的对话历史

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    if not db_choice:
        return jsonify({'error': 'No database selected'}), 400

    # 获取用户的对话历史
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    if is_sql_query:
        table_structure = get_table_structure(db_choice)
        sql_query = get_sql_query_from_natural_language(question, table_structure, chat_histories[user_id])
        try:
            results = query_database(sql_query, db_choice)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        Table = PrettyTable()
        for row in results:
            Table.add_row(row)
        results_table = Table.get_html_string(header = False)
        results_str = "\n".join([str(row) for row in results])
        # Save SQL query and results in chat history
        chat_histories[user_id].append({"role": "user", "content": question})
        chat_histories[user_id].append({"role": "assistant", "content": f"SQL Query:\n{sql_query}\n\nResults:\n{results_str}"})

        return jsonify({'sql_query': sql_query, 'results': results_str, 'table': results_table})
    
    else:
        chat_history = chat_histories.get(user_id, [])

        messages = [
            ("system", "You are a conversational assistant. Respond to the user's query based on the provided context.If there exist SQL Query and the results that related to the database in the context,and the question is related to the infomation of the results,your answer must base on the database result!"),
        ] + chat_history + [("human", question)]

        response = llm.invoke(messages)
        reply = response.content.strip()

        # 更新对话历史
        chat_histories[user_id].append({"role": "human", "content": question})
        chat_histories[user_id].append({"role": "assistant", "content": reply})

        return jsonify({'results': reply})

# 发送数据到图表
@app.route('/send_to_graph', methods=['POST'])
def send_to_graph():
    data = request.json
    query = data.get('query')
    results = data.get('results')
    database = data.get('database')

    if not query or not results or not database:
        return jsonify({'error': 'Invalid input'}), 400

    # 保存数据到会话，以便后续处理
    session['current_data'] = results
    session['current_query'] = query
    session['selected_database'] = database

    return jsonify({'status': 'success'})

# 处理聊天记录中的数据
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    data = request.json
    received_data = data.get('received_data')
    user_message = data.get('user_message')
    plot_type = data.get('plot_type')

    if not received_data or not user_message or not plot_type:
        return jsonify({'error': 'Missing required fields'}), 400

    # Pass the received_data and user_message to the generate_plot function
    result = generate_plot(user_message, received_data, plot_type)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify({'img_url': result['img_url'], 'analysis': result['analysis']})


# 进一步分析
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    data_str = data.get('data')
    follow_up_query = data.get('query')
    
    if not data_str or not follow_up_query:
        return jsonify({'error': 'Missing data or query'}), 400

    # 处理进一步的分析
    analysis_result = get_analysis_from_data(data_str, follow_up_query)
    
    return jsonify({'analysis_result': analysis_result})

if __name__ == '__main__':
    app.run(debug=True)
