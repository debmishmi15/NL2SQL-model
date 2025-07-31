import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from sqlalchemy import create_engine, text
import pandas as pd

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Database connection 
db_uri = "mysql+pymysql://root:Mishmi#2023@localhost/fraud_detection"
engine = create_engine(db_uri)

# generate SQL
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
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    return sql_query

# execute SQL query
def execute_sql(sql_query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            data = result.fetchall()
            columns = result.keys()
            return data, columns
    except Exception as e:
        return f"Error: {e}", None

# Streamlit UI config
st.set_page_config(page_title="NL2SQL Chat Assistant")

st.title("Natural Language to SQL Chat Assistant")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(f"**Generated SQL:**\n```sql\n{chat['sql']}\n```")
        if isinstance(chat["result"], str):
            st.error(chat["result"])
        elif chat["result"]:
            df = pd.DataFrame(chat["result"], columns=chat["columns"])
            st.dataframe(df)
        else:
            st.info("No records found.")

# User input at bottom
user_query = st.chat_input("Type your natural language query here...")

# If user sends a query
if user_query:
    sql_query = generate_sql(user_query)
    result, columns = execute_sql(sql_query)

    # Store in chat history
    st.session_state.chat_history.append({
        "user": user_query,
        "sql": sql_query,
        "result": result,
        "columns": columns
    })

    # Rerun app to display new chat
    st.rerun()

