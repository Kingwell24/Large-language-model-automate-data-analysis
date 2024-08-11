from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from lc import get_sql_query_from_natural_language, query_database, get_table_structure, get_analysis_from_data, generate_plot
import pandas as pd

app = Flask(__name__)

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
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template('web_ask.html')

@app.route('/main/graph_showing')
def graph_showing_page():
    return render_template('graph_showing.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
        except mysql.connector.Error as err:
            cursor.close()
            conn.close()
            return jsonify({'message': f'Error: {err}'}), 500
        
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
            conn.commit()
            flash('User created successfully. Please log in.', 'success')
            return redirect(url_for('signin'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # 获取数据库结构
    table_structure = get_table_structure()

    # 生成 SQL 查询
    sql_query = get_sql_query_from_natural_language(question, table_structure)

    try:
        # 执行 SQL 查询
        results = query_database(sql_query)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # 将查询结果转换为字符串
    results_str = "\n".join([str(row) for row in results])

    return jsonify({'sql_query': sql_query, 'results': results_str})



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
        df = pd.DataFrame(results)
        img_url = generate_plot(df, plot_type)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'img_url': img_url})


if __name__ == '__main__':
    app.run(debug=True)