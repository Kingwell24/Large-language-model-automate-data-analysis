document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.querySelector('#submit-query-btn');
    const sqlQueryButton = document.querySelector('#sql-query-btn');
    const inputField = document.querySelector('#query-input');
    const responseMessageContainer = document.querySelector('#response-message');
    const Database1Btn = document.getElementById('northwind-btn');
    const Database2Btn = document.getElementById('co2-btn');
    const databaseSelection = document.getElementById('database-selection');
    const inputArea = document.querySelector('.input-area');
    const responseArea = document.querySelector('.response');
    const userId = localStorage.getItem('user_id') || new Date().getTime(); // 使用时间戳作为 user_id
    localStorage.setItem('user_id', userId);

    let selectedDatabase = '';
    let chatHistory = []; // 存储聊天记录

    // 选择数据库函数
    function selectDatabase(database) {
        selectedDatabase = database;
        databaseSelection.style.display = 'none'; // 隐藏选择数据库的按钮
        inputArea.style.display = 'flex'; // 显示输入区域
        responseMessageContainer.style.display = 'block'; // 显示响应区域

        // 获取并显示表结构信息
        fetch('/table_structure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ database: selectedDatabase })
        })
        .then(response => response.json())
        .then(data => {
            if (data.table_structure) {
                const tableStructureElement = document.createElement('div');
                tableStructureElement.classList.add('message', 'response');
                tableStructureElement.innerHTML = `<strong>Table Structure:</strong><br>${data.table_structure}`;
                responseMessageContainer.appendChild(tableStructureElement);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessageElement = document.createElement('div');
            errorMessageElement.classList.add('message', 'response');
            errorMessageElement.textContent = 'An error occurred while retrieving table structure.';
            responseMessageContainer.appendChild(errorMessageElement);
        });
    }

    // 选择数据库按钮的示例代码
    Database1Btn.addEventListener('click', function() {
        selectDatabase('northwind');
    });

    Database2Btn.addEventListener('click', function() {
        selectDatabase('co2');
    });


    // 发送消息函数
    function sendMessage(isSqlQueryRequest) {
        const message = inputField.value.trim();

        if (message === '') {
            return;
        }

        // 将消息显示在聊天框中
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'user');
        userMessageElement.textContent = message;
        responseMessageContainer.appendChild(userMessageElement);

        // 发送消息到服务器
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: message,
                database: selectedDatabase,
                is_sql_query: isSqlQueryRequest,
                user_id: userId
            })
        })
        .then(response => response.json())
        .then(data => {
            // Append the results
            //const resultsElement = document.createElement('div');
            //resultsElement.classList.add('message', 'response');
            //resultsElement.textContent = `Results:\n${data.results}`;
            //responseMessageContainer.appendChild(resultsElement);
        
            // Append the SQL query if it's a SQL Query request
            if (isSqlQueryRequest) {
                const table = document.createElement('div');
                table.classList.add('message', 'response');
                table.innerHTML = data.table;
                responseMessageContainer.appendChild(table);

                const sqlQueryElement = document.createElement('div');
                sqlQueryElement.classList.add('message', 'response');
                sqlQueryElement.textContent = `SQL Query:\n${data.sql_query}`;
                responseMessageContainer.appendChild(sqlQueryElement);

                // Add "Send to Graph Showing" button
                const sendToGraphButton = document.createElement('button');
                sendToGraphButton.textContent = 'Send to Graph Showing';
                sendToGraphButton.classList.add('send-to-graph-btn');
                responseMessageContainer.appendChild(sendToGraphButton);

                sendToGraphButton.addEventListener('click', () => {
                    fetch('/send_to_graph', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            query: data.sql_query,
                            results: data.results,
                            database: selectedDatabase
                        })
                    })
                    .then(response => response.json())
                    .then(responseData => {
                        if (responseData.status === 'success') {
                            // Store data in sessionStorage
                            sessionStorage.setItem('graph_data', JSON.stringify({
                                query: data.sql_query,
                                results: data.results,
                                database: selectedDatabase,
                                table: data.table
                            }));
                
                            const successMessage = document.createElement('div');
                            successMessage.classList.add('message', 'response');
                            successMessage.textContent = 'Data sent to graph showing page successfully.';
                            responseMessageContainer.appendChild(successMessage);
                
                            // Redirect to the graph showing page
                            window.location.href = 'graph_showing'; // or use appropriate URL
                        } else {
                            const errorMessageElement = document.createElement('div');
                            errorMessageElement.classList.add('message', 'error');
                            errorMessageElement.textContent = responseData.error || 'Failed to send data to graph showing page.';
                            responseMessageContainer.appendChild(errorMessageElement);
                        }
                    })
                    .catch(error => {
                        console.log('Error:', error);
                        const errorMessageElement = document.createElement('div');
                        errorMessageElement.classList.add('message', 'error');
                        errorMessageElement.textContent = 'An error occurred while sending data to graph showing page.';
                        responseMessageContainer.appendChild(errorMessageElement);
                    });
                });
                
            }

            else{
            // Append the results
                const resultsElement = document.createElement('div');
                resultsElement.classList.add('message', 'response');
                resultsElement.textContent = `Results:\n${data.results}`;
                responseMessageContainer.appendChild(resultsElement);
            }
        
            // Append the image if available
            if (data.image_url) {
                const imageElement = document.createElement('img');
                imageElement.src = `${data.image_url}?t=${new Date().getTime()}`;
                imageElement.alt = "Response Image";
                imageElement.style.maxWidth = "100%"; // 确保图像适合容器
                responseMessageContainer.appendChild(imageElement);
            }
        
            // Scroll to the latest message
            responseMessageContainer.scrollTop = responseMessageContainer.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessageElement = document.createElement('div');
            errorMessageElement.classList.add('message', 'error');
            errorMessageElement.textContent = '发送消息时发生错误。';
            responseMessageContainer.appendChild(errorMessageElement);
        });

        // 清空输入框
        inputField.value = '';
    }

    // 点击发送按钮事件处理
    sendButton.addEventListener('click', function() {
        sendMessage(false); // 发送普通请求
    });

    // 点击 SQL Query 按钮事件处理
    sqlQueryButton.addEventListener('click', function() {
        sendMessage(true); // 发送 SQL Query 请求
    });

    // 监听键盘按下事件
    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // 阻止默认行为
            sendMessage(false); // 调用发送消息函数
        }
    });
});