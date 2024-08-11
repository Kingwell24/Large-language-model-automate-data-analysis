document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.querySelector('.input-area button');
    const inputField = document.querySelector('.input-area input');
    const messagesContainer = document.querySelector('.messages');

    // 发送消息函数
    function sendMessage() {
        const message = inputField.value;

        if (message.trim() === '') {
            return;
        }

        // 将消息显示在聊天框中
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'user');
        userMessageElement.textContent = message;
        messagesContainer.appendChild(userMessageElement);

        // 发送消息到服务器
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                const errorMessageElement = document.createElement('div');
                errorMessageElement.classList.add('message', 'response');
                errorMessageElement.textContent = data.error;
                messagesContainer.appendChild(errorMessageElement);
            } else {
                const responseMessageElement = document.createElement('div');
                responseMessageElement.classList.add('message', 'response');
                responseMessageElement.textContent =JSON.stringify(data.results);
                messagesContainer.appendChild(responseMessageElement);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // 清空输入框
        inputField.value = '';
    }

    // 点击发送按钮事件处理
    sendButton.addEventListener('click', sendMessage);

    // 监听键盘按下事件
    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') { // 检查按下的是否是 Enter 键
            event.preventDefault(); // 阻止默认行为（比如换行）
            sendMessage(); // 调用发送消息函数
        }
    });
});
