document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessageDiv = document.getElementById('error-message');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();  // 防止默认表单提交行为

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // 清除之前的错误信息
        errorMessageDiv.textContent = '';

        // 表单数据
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch('/signin', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                }
            });

            if (response.ok) {
                // 检查响应内容，如果登录成功，重定向到主页
                document.getElementById('username').value = '';  // 清空输入框
                document.getElementById('password').value = '';  // 清空输入框
                window.location.href = '/main/ask';
            } else {
                // 处理服务器返回的错误
                const error = await response.json();
                errorMessageDiv.textContent = `Login failed: ${error.error}`;
                errorMessageDiv.style.display = 'block';  // 显示错误信息
            }
        } catch (error) {
            // 处理请求失败的错误
            errorMessageDiv.textContent = `An error occurred: ${error.message}`;
            errorMessageDiv.style.display = 'block';  // 显示错误信息
        }
    });
});
