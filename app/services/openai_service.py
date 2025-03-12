from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_sql_query(self, user_query, table_schemas):
        """Generate SQL query based on user question and table schemas."""
        schemas_json = json.dumps(table_schemas)
        
        prompt = f"""
        You are a helpful SQL assistant.
        
        Given the following database schema:
        {schemas_json}
        
        Generate a SQL query to answer this question: {user_query}
        
        Provide ONLY the SQL query without any explanations or comments.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a SQL expert that generates accurate MySQL queries based on schema information and user questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()

    def generate_response(self, user_query, sql_query, sql_result):
        """Generate a natural language response based on SQL results."""
        prompt = f"""
        User question: {user_query}
        
        SQL query used: {sql_query}
        
        Query result: {json.dumps(sql_result)}
        
        Please provide a clear, concise answer to the user's question based on these results.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains database query results in natural language."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()

openai_service = OpenAIService()
