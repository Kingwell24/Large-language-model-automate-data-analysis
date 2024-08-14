from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from lc import llm,get_sql_query_from_natural_language, query_database, get_table_structure, get_analysis_from_data, generate_plot
import pandas as pd
import datetime

app = Flask(__name__) 

chat_histories = {} # 用于存储聊天记录

app.secret_key = os.urandom(24)  # 生成一个随机的 24 字节的密钥

# MySQL 配置
db_config = {
    'user': 'root',
    'password': 'Wzx20071201',
    'host': 'localhost',
    'database': 'Microsoft_ai_data_analyse_flask_signin'
}

# 连接 MySQL 数据库
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

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


# @app.route('/signin', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
        
#         try:
#             cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
#             user = cursor.fetchone()
#         except mysql.connector.Error as err:
#             cursor.close()
#             conn.close()
#             return jsonify({'message': f'Error: {err}'}), 500
        
#         cursor.close()
#         conn.close()

#         if user and check_password_hash(user['password_hash'], password):
#             session['username'] = username
#             return jsonify({'message': 'Login successful'}), 200
#         else:
#             return jsonify({'message': 'Invalid username or password'}), 401

#     return render_template('signin.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('signin'))

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         password_hash = generate_password_hash(password)

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         try:
#             cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
#             conn.commit()
#             flash('User created successfully. Please log in.', 'success')
#             return redirect(url_for('signin'))
#         except mysql.connector.Error as err:
#             flash(f'Error: {err}', 'error')
#         finally:
#             cursor.close()
#             conn.close()

#     return render_template('signup.html')

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

        results_str = "\n".join([str(row) for row in results])
        # Save SQL query and results in chat history
        chat_histories[user_id].append({"role": "user", "content": question})
        chat_histories[user_id].append({"role": "assistant", "content": f"SQL Query:\n{sql_query}\n\nResults:\n{results_str}"})

        return jsonify({'sql_query': sql_query, 'results': results_str})
    
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


@app.route('/plot', methods=['POST'])
def plot():
    data = request.json
    query = data.get('query')
    plot_type = data.get('plot_type')
    db_choice = data.get('database')
    
    if not query or not plot_type:
        return jsonify({'error': 'Missing query or plot type'}), 400

    table_structure = get_table_structure(db_choice)
    sql_query = get_sql_query_from_natural_language(query, table_structure)

    try:
        results = query_database(sql_query, db_choice)
        print(results)
        df = pd.DataFrame(results)
        print(df)
        img_url = generate_plot(df, plot_type)
        print(img_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'img_url': img_url})


if __name__ == '__main__':
    app.run(debug=True)