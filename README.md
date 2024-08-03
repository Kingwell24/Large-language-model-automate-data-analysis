# Automated Data Analysis with Large Language Models

Welcome to the Automated Data Analysis project! This project leverages large language models to transform natural language queries into SQL queries, execute them on a MySQL database, and present the results in an interactive and insightful manner. Our system is designed to simplify data analysis and visualization, making it accessible to everyone, even without extensive SQL or programming knowledge.

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

     

## 🚀 How It Works

1. **User Input**: Enter your natural language query on the frontend.

2. **Query Processing**: The backend converts your input into an SQL query using a large language model.

3. **Data Retrieval**: The SQL query is executed on the MySQL database, and the results are fetched.

4. **Result Display**: Results are presented in a table format on the frontend.

5. **Further Analysis**: Optionally, request visualizations or additional data analysis.

   

## 📦 Getting Started

To get your development environment set up, follow these instructions:

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Kingwell24/Large-language-model-automate-data-analysis.git
cd your-repository
```

### 2. Set Up Your MySQL Database

1. **Install MySQL**: If you don’t have MySQL installed, you can download and install it from [MySQL's official website](https://dev.mysql.com/downloads/mysql/). Follow the installation instructions for your operating system.

2. **Create a Database**: Create the necessary databases and tables for your project. You might use the following SQL commands to set up your `northwind` and `weather_forecast` databases:

   ```sql
   CREATE DATABASE northwind;
   USE northwind;
   -- Add your table creation commands here
   
   CREATE DATABASE weather_forecast;
   USE weather_forecast;
   -- Add your table creation commands here
   ```

3. **Configure Database Access**: Update the `db_config` dictionary in your code with the appropriate credentials for your MySQL databases. The configuration should include the host, user, password, and database names:

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

### 3. Configure the GPT API Interface

1. **Obtain API Credentials**: You need to have an Azure OpenAI account. Obtain your API key and endpoint URL from the Azure portal.

2. **Set Up Environment Variables**: Create a `.env` file in the root directory of your project or set the environment variables directly in your system. Add the following variables:

   ```bash
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview
   ```

   Make sure to replace `your_api_key` and `your-endpoint` with your actual API key and endpoint.

### 4. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```
pip install langchain mysql-connector-python mysql pandas matplotlib seaborn
```



## 🛠️ Tools & Libraries

- **Python**: Main programming language.
- **Flask**: Web framework for the frontend.
- **LangChain**: Large language model library for natural language processing.
- **MySQL**: Database management system.
- **Pandas, Matplotlib, Seaborn**: Libraries for data manipulation and visualization.



## 📬 Contact

For questions or contributions, please reach out to 3118497634@qq.com or open an issue in the repository.
