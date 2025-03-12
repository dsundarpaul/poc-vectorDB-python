# import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiService:
    def __init__(self):

        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        
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
          model="gemini-2.0-flash", contents=prompt
        )
        print(response.text)
        
        # response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_response(self, user_query, sql_query, sql_result):
        """Generate a natural language response based on SQL results."""
        prompt = f"""
        User question: {user_query}
        
        SQL query used: {sql_query}
        
        Query result: {json.dumps(sql_result)}
        
        Please provide a clear, concise answer to the user's question based on these results.
        """
        
        # response = self.model.generate_content(prompt)
        # return response.text.strip()
    
        response = self.client.models.generate_content(
          model="gemini-2.0-flash", contents=prompt
        )
        return response.text.strip()

gemini_service = GeminiService()