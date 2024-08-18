# Automated Data Analysis with Large Language Models

This project leverages large language models to transform natural language queries into SQL queries, execute them on a MySQL database, and present the results in an interactive and insightful manner. Our system is designed to simplify data analysis and visualization, making it accessible to everyone, even without extensive SQL or programming knowledge.

## 🛠️ Features

1. **Natural Language Querying**
   Simply type your questions or requests in natural language. No matter is a simple "Show all sales data for 2023" query or one that is   way more complicated "Show me the names of companies in the city for the second quarter of 2023, where the company names start with 'A' and the sales exceed 10,000. Additionally, provide the names and contact information of the company representatives based on their reports." Our system converts these queries into precise SQL statements according to your given database.

2. **SQL Query Execution**
   Automatically executes the generated SQL queries against a MySQL database, retrieving the relevant data seamlessly.

3. **Data Display**
   Displays query results in a well-structured table format on the frontend. Users can easily view and download the data.

4. **Advanced Data Analysis & Visualization**
   Request further analysis or generate various types of charts based on the retrieved data. Whether you need a line chart, scatter plot, or pie chart, our system can handle it.

   

## 🖥️ Technical Architecture

1. **Frontend**

   - **Technology**: HTML-based UI using Flask framework.
   - **Components**: Natural language input, SQL query conversion, result display, and chart visualization.

2. **Backend**

   - **Technology**: Azure ChatGPT for natural language processing and SQL query generation.
   - **Components**: Receives user input, generates SQL queries, executes them, and returns results.

3. **Database**

   - **Technology**: MySQL for data storage.
   - **Components**: Stores project and sample data for querying.

4. **Large Language Model**

   - **Library**: LangChain for natural language processing and SQL query generation.

     

## 📦 How to run locally

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Kingwell24/Large-language-model-automate-data-analysis.git
```

Or you can just download the zip and unzip it to whichever path you want.

### 2. Set Up Your MySQL Database

1. **Install MySQL**: If you don’t have MySQL installed, you can download and install it from [MySQL's official website](https://dev.mysql.com/downloads/mysql/). Follow the installation instructions for your operating system.Then import the database you want to analyse into your MySQL.

2. **Configure Database Access**: Update the `db_config` dictionary in `lc.py` with the appropriate credentials for your MySQL databases. The configuration should include the host, user, password, and database names:

   ```python
   db_config = {
       'northwind': {
           'host': "localhost",
           'user': "root",
           'password': "your_password",
           'database': "northwind"
       },
       'weather_forecast': {
           'host': "localhost",
           'user': "root",
           'password': "your_password",
           'database': "weather_forecast"
       }
   }
   ```

3. **Configure Database connection**: Update the `get_db_connection` dictionary in `lc.py` with the appropriate credentials for the MySQL databases you want to connect to. The configuration should include the host, user, password, and database names:

   ```python
   def get_db_connection(database):
       if database == "northwind":
           return mysql.connector.connect(
               host="localhost",
               user="root",
               password="52zz468275",
               database="northwind")
       elif database == "weather_forecast":
           return mysql.connector.connect(
               host="localhost",
               user="root",
               password="52zz468275",
               database="weather_forecast"
       )
   ```

### 3. Configure the GPT API Interface

1. **Obtain API Credentials**: You need to have an Azure OpenAI account. Obtain your API key and endpoint URL from the Azure portal.

2. **Set Up GPT API Interface**:  Find the GPT environment setting part in `lc.py`,and add your api key into the configuration:

   ```bash
   os.environ["AZURE_OPENAI_API_KEY"] = "your_api_key"
   os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-"
   ```


   3.**Configure langchain deployment**: Commonly when you get your api,the following config are set,just remember to reset some of the parameters as follows:

```python
llm = AzureChatOpenAI(
    azure_deployment="https://your-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
    api_version="your_version",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
```

### 4. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```
pip install Flask mysql-connector-python werkzeug pandas python-dotenv matplotlib seaborn langchain azure-openai
```

**After all this configuration are set , run app.py , then access http://127.0.0.1:5000 on your browser.** 

## 🛠️ Tools & Libraries

- **Python**: Main programming language.
- **Flask**: Web framework for the frontend.
- **LangChain**: Large language model library for natural language processing.
- **MySQL**: Database management system.
- **Pandas, Matplotlib, Seaborn**: Libraries for data manipulation and visualization.



## 📬 Contact

For questions or contributions, please reach out to 3118497634@qq.com or open an issue in the repository.
