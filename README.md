# Natural Language to SQL Query Assistant (AI-Powered)

A Streamlit-based chatbot application that converts natural language queries into SQL, executes them on a MySQL database, and displays results — powered by Google's Gemini 1.5 Flash model via the Generative AI API.


## Features:

- Converts plain English questions into SQL queries
- Executes queries on a live MySQL database
- Displays query results in an interactive, chat-style interface
- Maintains full chat history like a chatbot
- Clean, minimal Streamlit UI for ease of use
- AI backend powered by Gemini (Gemini 1.5 Flash)


## Tech Stack:

- Python 3.12+
- Streamlit
- Google Generative AI API (Gemini)
- MySQL
- SQLAlchemy
- PyMySQL
- dotenv


## Project Structure:
Your project folder\n
│\n
├── app.py\n 
├── main.py\n 
├── db_setup.sql\n 
├── test_data.sql\n 
├── .env\n 
├── requirements.txt\n 
└── README.md\n 

## Setup Instructions:

### 1️. Install Dependencies
    pip install -r requirements.txt

### 2️. Set Your API Key 
    Create a .env file in your project directory:
    GEMINI_API_KEY=your_gemini_api_key_here

### 3️. Set Up Database
    Setup your database in db_setup.sql as per your tables and requirements (schema).
    Run db_setup.sql inside MySQL Workbench or CLI to create your schema and tables.
    (Optionally) Run test_data.sql to insert sample records for testing.


## How to Run:
### Run the chatbot UI:
    streamlit run app.py








