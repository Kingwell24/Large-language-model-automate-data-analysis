document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.getElementById('submit-query-btn');
    const inputField = document.getElementById('query-input');
    const responseMessage = document.getElementById('response-message');
    const data = JSON.parse(sessionStorage.getItem('graph_data'));
    // 获取图表类型
    const plotType = document.getElementById('plot_type').value;

    // 初始化以及回显接收到的数据
    function initialize() {
        if (data) {
            const Table = data.table;
            const responseMessageContainer = document.querySelector('#response-message');
            const resultsElement = document.createElement('div');
            resultsElement.classList.add('message', 'response');
            // resultsElement.textContent = `Received Data: ${results}`;
            // responseMessageContainer.appendChild(resultsElement);
            resultsElement.innerHTML = Table;
            responseMessageContainer.appendChild(resultsElement);

            // Optionally clear the stored data if needed
            sessionStorage.removeItem('graph_data');
        } else {
            console.error('No data found in sessionStorage.');
        }
    }

// Send chart generation request
function sendMessage() {
    const message = inputField.value.trim();
    if (message === '') return;

    // 获取选择的图表类型
    const plotType = document.getElementById('plot_type').value;
    const plotchoiceElement = document.createElement('div');
    plotchoiceElement.classList.add('message', 'user');
    plotchoiceElement.textContent = `Chosen plot type:\n${plotType}`;
    responseMessage.appendChild(plotchoiceElement);

    // 将要求显示在聊天框中
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user');
    userMessageElement.textContent = message;
    responseMessage.appendChild(userMessageElement);

    // 获取结果数据
    const results = data.results;
    if (!results) {
        const errorMessageElement = document.createElement('div');
        errorMessageElement.classList.add('message', 'error');
        errorMessageElement.textContent = 'No data available to process.';
        responseMessage.appendChild(errorMessageElement);
        return;
    }

    // 发送图表请求到后端
    const requestBody = {
        received_data: `Received Data: ${results}`,
        user_message: message,
        plot_type: plotType
    };

    fetch('/generate_chart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
        // 显示图表
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

            // 显示分析报告
            const analysisElement = document.createElement('div');
            analysisElement.classList.add('message', 'analysis');
            analysisElement.innerHTML = `Analysis Report:<br>${data.analysis.replace(/\n/g, '<br>')}<br>If you need more further analysis, return back to ask webpage to achieve it.`;
            responseMessage.appendChild(analysisElement);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const errorMessageElement = document.createElement('div');
        errorMessageElement.classList.add('message', 'error');
        errorMessageElement.textContent = 'An error occurred while processing the request.';
        responseMessage.appendChild(errorMessageElement);
    });

    inputField.value = '';
}



    // Initialize on page load
    initialize();

    sendButton.addEventListener('click', sendMessage);

    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior
            sendMessage();
        }
    });
});