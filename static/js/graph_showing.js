document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.getElementById('submit-query-btn');
    const inputField = document.getElementById('query-input');
    const responseMessage = document.getElementById('response-message');
    const northwindBtn = document.getElementById('northwind-btn');
    const weatherForecastBtn = document.getElementById('weatherforecast-btn');
    const databaseSelection = document.getElementById('database-selection');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    let selectedDatabase; // 确保 selectedDatabase 在全局范围内定义

    // 发送消息函数
    function sendMessage() {
        const message = inputField.value.trim();
        if (message === '' || !selectedDatabase) return;
    
        // 隐藏发送按钮
        sendButton.style.display = 'none';
    
        // 清空之前的响应消息
        responseMessage.innerHTML = '';
    
        // 显示用户输入的消息
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'user');
        userMessageElement.textContent = message;
        responseMessage.appendChild(userMessageElement);
    
        // 发送消息到服务器
        fetch('/plot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                query: message, 
                plot_type: 'bar',
                database: selectedDatabase  // 传递选择的数据库
            })  // 默认图表类型为 bar
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // 显示错误消息
                const errorMessageElement = document.createElement('div');
                errorMessageElement.classList.add('message', 'error');
                errorMessageElement.textContent = data.error;
                responseMessage.appendChild(errorMessageElement);
            } else {
                // 显示返回的数据
                const responseMessageElement = document.createElement('div');
                responseMessageElement.classList.add('message', 'response');
                responseMessageElement.innerHTML = `<img src="${data.img_url}" alt="Generated Plot" />`;
                responseMessage.appendChild(responseMessageElement);
    
                // 显示图表选择按钮
                const responseButtonsElement = document.createElement('div');
                responseButtonsElement.classList.add('response-buttons');
                responseButtonsElement.innerHTML = `
                    <button id="bar-chart-btn">Bar Chart</button>
                    <button id="line-chart-btn">Line Chart</button>
                    <button id="pie-chart-btn">Pie Chart</button>
                    <button id="scatter-chart-btn">Scatter Chart</button>
                `;
                responseMessage.appendChild(responseButtonsElement);
    
                // 为动态生成的按钮添加事件监听器
                document.getElementById('bar-chart-btn').addEventListener('click', () => handleChartSelection('bar'));
                document.getElementById('line-chart-btn').addEventListener('click', () => handleChartSelection('line'));
                document.getElementById('pie-chart-btn').addEventListener('click', () => handleChartSelection('pie'));
                document.getElementById('scatter-chart-btn').addEventListener('click', () => handleChartSelection('scatter'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    
        // 清空输入框
        inputField.value = '';
    }
    
    function handleDatabaseSelection(database) {
        selectedDatabase = database; // 将选择的数据库存储在变量中
        console.log('Selected database:', database); // 打印所选数据库的信息
        databaseSelection.style.display = 'none';
    }
    
    northwindBtn.addEventListener('click', () => handleDatabaseSelection('northwind'));
    weatherForecastBtn.addEventListener('click', () => handleDatabaseSelection('weather_forecast'));

    // 点击按钮发送消息
    sendButton.addEventListener('click', sendMessage);

    // 按下 Enter 键发送消息
    inputField.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // 防止默认行为（如提交表单）
            sendMessage();
        }
    });

    function handleChartSelection(chartType) {
        const message = inputField.value.trim();
        if (message === '') return;

        // 发送请求以生成所选类型的图表
        fetch('/plot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                query: message, 
                plot_type: chartType,
                database: selectedDatabase // 保持数据库选择的一致性
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                // 更新图表
                const responseMessageElement = document.createElement('div');
                responseMessageElement.classList.add('message', 'response');
                responseMessageElement.innerHTML = `<img src="${data.img_url}" alt="Generated Plot" />`;
                responseMessage.appendChild(responseMessageElement);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
