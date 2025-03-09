# import ollama

# def generate_sql(user_input):
#     prompt = f"""
#     Convert the following plain text request into an SQL query. Only return the SQL query without any explanation.
    
#     User: {user_input}
#     SQL Query:
#     """
#     response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
#     return response['message']['content']

# # Example Usage
# while True:
#     user_input = input("Ask a SQL Query (or type 'exit' to quit): ")
#     if user_input.lower() == "exit":
#         break
#     sql_query = generate_sql(user_input)
#     print("\nGenerated SQL Query:\n", sql_query, "\n")


import streamlit as st
import ollama

def generate_sql(user_input):
    prompt = f"""
    Convert the following plain text request into an SQL query. Only return the SQL query without any explanation.
    
    User: {user_input}
    SQL Query:
    """
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Streamlit UI
st.title("🛠️ SQL Query Generator")
st.write("Enter a natural language query, and I'll generate the SQL query for you!")

user_input = st.text_area("Ask a SQL Query:", height=100)

if st.button("Generate SQL"):
    if user_input.strip():
        sql_query = generate_sql(user_input)
        st.code(sql_query, language="sql")
    else:
        st.warning("Please enter a query.")
