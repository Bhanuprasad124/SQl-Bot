import streamlit as st
import mysql.connector
import ollama

# --- Streamlit UI ---
st.set_page_config(page_title="SQL Query Bot", layout="centered")

st.title("🤖 SQL Query Generator & Executor")

# --- Database Connection Form ---
st.sidebar.header("🔗 Database Connection")

host = st.sidebar.text_input("Host", value="localhost")
user = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
DATABASE_NAME = st.sidebar.text_input("Database Name")

connect_btn = st.sidebar.button("Connect to Database")


def generate_sql(user_input):
    prompt = f"""
        Convert the following plain text request into an SQL query.
    
    - The database name is `{DATABASE_NAME}`.
    - Always use the format `{DATABASE_NAME}.table_name` instead of just `table_name`.
    - Do NOT provide explanations, only return the SQL query.

    User: {user_input}
    SQL Query:
    """
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to execute SQL query on the database
def execute_sql_query(sql_query):
    try:
        # Connect to MySQL Database (Replace with your details)
        conn = mysql.connector.connect(
            host=host,  # Change if using a cloud database
            user=user,       # Your DB username
            password=password,  # Your DB password
            database=DATABASE_NAME# Your Database name
        )
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(sql_query)
        rows = cursor.fetchall()  # Fetch all results

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        # Close the connection
        cursor.close()
        conn.close()

        return column_names, rows  # Return column names + data
    except Exception as e:
        return None, str(e)  # Return error message if query fails

# Streamlit UI

st.write("Enter a plain text request, and I'll generate the SQL query and fetch the data for you!")

user_input = st.text_area("Ask a SQL Query:", height=100)

if st.button("Generate & Execute SQL"):
    if user_input.strip():
        sql_query = generate_sql(user_input)  # Generate SQL
        st.code(sql_query, language="sql")  # Show generated SQL

        # Execute SQL and display results
        columns, data = execute_sql_query(sql_query)
        if columns:
            st.write("### Query Results:")
            st.dataframe([dict(zip(columns, row)) for row in data])  # Display data as table
        else:
            st.error(f"Error executing query: {data}")
    else:
        st.warning("Please enter a query.")
