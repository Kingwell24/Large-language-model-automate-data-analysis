import os

os.environ["AZURE_OPENAI_API_KEY"] = "e06b809982f3483fa42cc907daf923df"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"


from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment="https://bySanpingLi.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
    api_version="2023-03-15-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

messages = [
    ("system", "You are a helpful assistant that generate SQL query. Generate the user's query."),
    ("human", "生成基于northwind数据库的SQL查询语句：查询每个订单的订单ID、订单日期、客户名称和员工姓名。"),
]

response = llm.invoke(messages)
print(response)
print(response.content)
