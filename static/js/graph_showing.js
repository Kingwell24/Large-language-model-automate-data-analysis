document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.getElementById('submit-query-btn');
    const inputField = document.getElementById('query-input');
    const responseMessage = document.getElementById('response-message');
    const northwindBtn = document.getElementById('northwind-btn');
    const weatherForecastBtn = document.getElementById('weatherforecast-btn');
    const databaseSelection = document.getElementById('database-selection');

    let selectedDatabase;
    let currentMessage = ''; // 用于存储当前显示的问题

    function sendMessage() {
        const message = inputField.value.trim();
        if (message === '' || !selectedDatabase) return;
    
        sendButton.style.display = 'none';
        currentMessage = message; // 存储当前问题
    
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'user');
        userMessageElement.textContent = message;
        responseMessage.appendChild(userMessageElement);
    
        fetch('/plot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                query: message, 
                plot_type: 'line',
                database: selectedDatabase 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                const errorMessageElement = document.createElement('div');
                errorMessageElement.classList.add('message', 'error');
                errorMessageElement.textContent = data.error;
                responseMessage.appendChild(errorMessageElement);
            } else {
                const responseMessageElement = document.createElement('div');
                responseMessageElement.classList.add('message', 'response');
                responseMessageElement.innerHTML = `<img src="${data.img_url}" alt="Generated Plot" />`;
                responseMessage.appendChild(responseMessageElement);
    
                const responseButtonsElement = document.createElement('div');
                responseButtonsElement.classList.add('response-buttons');
                responseButtonsElement.innerHTML = `
                    <button id="bar-chart-btn">Bar Chart</button>
                    <button id="line-chart-btn">Line Chart</button>
                    <button id="pie-chart-btn">Pie Chart</button>
                    <button id="scatter-chart-btn">Scatter Chart</button>
                `;
                responseMessage.appendChild(responseButtonsElement);
    
                document.getElementById('bar-chart-btn').addEventListener('click', () => handleChartSelection('bar'));
                document.getElementById('line-chart-btn').addEventListener('click', () => handleChartSelection('line'));
                document.getElementById('pie-chart-btn').addEventListener('click', () => handleChartSelection('pie'));
                document.getElementById('scatter-chart-btn').addEventListener('click', () => handleChartSelection('scatter'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    
        inputField.value = '';
    }
    
    function handleDatabaseSelection(database) {
        selectedDatabase = database;
        console.log('Selected database:', database);
        databaseSelection.style.display = 'none';
    }
    
    northwindBtn.addEventListener('click', () => handleDatabaseSelection('northwind'));
    weatherForecastBtn.addEventListener('click', () => handleDatabaseSelection('weather_forecast'));

    sendButton.addEventListener('click', sendMessage);

    inputField.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    function handleChartSelection(chartType) {
        if (currentMessage === '') return; // 使用存储的当前问题

        fetch('/plot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                query: currentMessage,  // 使用当前问题
                plot_type: chartType,
                database: selectedDatabase 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
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
