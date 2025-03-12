
from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class GoogleGenAIService:
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyCY3qHtiJreMoVfS2bXYUKoBcE_823YPE4")
    
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
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[
                {"role": "system", "content": "You are a SQL expert that generates accurate MySQL queries based on schema information and user questions."},
                {"role": "user", "content": prompt}
            ],
        )
        print('in g-genai service, generate_sql_query res', response.text)
        return response.text 
        # return response.choices[0].message.content.strip()

    def generate_response(self, user_query, sql_query, sql_result):
        """Generate a natural language response based on SQL results."""
        prompt = f"""
        User question: {user_query}
        
        SQL query used: {sql_query}
        
        Query result: {json.dumps(sql_result)}
        
        Please provide a clear, concise answer to the user's question based on these results.
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[
                {"role": "system", "content": "You are a helpful assistant that explains database query results in natural language."},
                {"role": "user", "content": prompt}
            ],
        )
        
        print('in g-genai service, generate_sql_query res', response.text)
        return response.text 

googlegenai_service = GoogleGenAIService()
