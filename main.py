from dotenv import load_dotenv
import os
import google.generativeai as genai
from sqlalchemy import create_engine, text

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini model with API key
genai.configure(api_key=api_key)
# model = genai.GenerativeModel('models/gemini-1.5-pro')
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Function to convert question to SQL (works when model= gemini-1.5-pro)
# def generate_sql(query):
#     prompt = f"Convert this natural language question into an SQL query:\n{query}\nSQL:"
#     response = model.generate_content(prompt)
#     return response.text.strip()

#when model= gemini-1.5-flash
def generate_sql(query):
    prompt = f"""
You are an AI assistant converting natural language questions into MySQL-compatible SQL queries. 

Here is the database schema:

Table: accounts(account_id, customer_name, customer_email, balance, open_date)
Table: transactions(transaction_id, account_id, amount, transaction_date, location, is_fraud)
Table: branches(branch_id, branch_name, location)

Now, convert this natural language question into an SQL query. 
Only return the SQL query — no explanations, no markdown formatting.

Question: {query}
"""
    response = model.generate_content(prompt)
    sql_query = response.text.strip()

    # Remove backticks and markdown code blocks if present
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query


# Connect to MySQL database (replace your_password with your actual password)
db_uri = "mysql+pymysql://root:Mishmi#2023@localhost/fraud_detection"
engine = create_engine(db_uri)

# Function to run SQL query
def execute_sql(sql_query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            return result.fetchall()
    except Exception as e:
        return f"Error: {e}"

# Main program execution
if __name__ == "__main__":
    # models = genai.list_models()
    # for m in models:
    #     print(m.name)

    # question = input("Enter your question: ")
    # sql_query = generate_sql(question)
    # print("Generated SQL:\n", sql_query)

    # result = execute_sql(sql_query)
    # print("Result:\n", result)

    while True:
        question = input("Your query: ")

        if question.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break

        sql_query = generate_sql(question)
        print("Generated SQL:\n", sql_query)

        result = execute_sql(sql_query)
        print("Result:")
        if isinstance(result, str):  # If it's an error message string
            print(result)
        elif result:
            for row in result:
                print(row)
        else:
            print("No records found.")

        print("\n-------------------------\n")

