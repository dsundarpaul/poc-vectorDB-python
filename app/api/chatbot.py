# from fastapi import APIRouter, Depends, HTTPException
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.services.vector_store import vector_store
# # from app.services.openai_service import openai_service
# from app.services.googlegenai_service import googlegenai_service
# from app.services.sql_service import sql_service

# router = APIRouter()

# class Query(BaseModel):
#     question: str

# @router.post("/ask")
# def ask_question(query: Query, db: Session = Depends(get_db)):
#     # Find relevant tables for the query
#     relevant_tables = vector_store.find_relevant_tables(query.question)
    
#     if not relevant_tables:
#         return {"answer": "I couldn't find relevant tables to answer your question."}
    
#     # Generate SQL query using OpenAI
#     sql_query = googlegenai_service.generate_sql_query(query.question, relevant_tables)
    
#     # Execute SQL query
#     query_result = sql_service.execute_query(sql_query)
    
#     if not query_result["success"]:
#         return {"answer": f"I encountered an error: {query_result['error']}"}
    
#     # Generate natural language response
#     response = googlegenai_service.generate_response(
#         query.question, 
#         sql_query, 
#         query_result["data"]
#     )
    
#     return {
#         "answer": response,
#         "sql_query": sql_query,
#         "query_result": query_result["data"],
#         "relevant_tables": [table["table_name"] for table in relevant_tables]
#     }

# @router.post("/initialize-vector-store")
# def initialize_vector_store():
#     result = vector_store.initialize_schema_embeddings()
#     return {"message": result}


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.vector_store import vector_store
from app.services.gemini_service import gemini_service
from app.services.sql_service import sql_service

router = APIRouter()

class Query(BaseModel):
    question: str

@router.post("/ask")
def ask_question(query: Query, db: Session = Depends(get_db)):
    # Find relevant tables for the query
    relevant_tables = vector_store.find_relevant_tables(query.question)

    # print('********************', relevant_tables)
    
    if not relevant_tables:
        return {"answer": "I couldn't find relevant tables to answer your question."}
    
    # Generate SQL query using Gemini
    sql_query = gemini_service.generate_sql_query(query.question, relevant_tables)
    
    # Execute SQL query
    query_result = sql_service.execute_query(sql_query)
    
    if not query_result["success"]:
        return {"answer": f"I encountered an error: {query_result['error']}"}
    
    # Generate natural language response
    response = gemini_service.generate_response(
        query.question, 
        sql_query, 
        query_result["data"]
    )
    
    return {
        "answer": response,
        "sql_query": sql_query,
        "query_result": query_result["data"],
        "relevant_tables": [table["table_name"] for table in relevant_tables]
    }

@router.post("/initialize-vector-store")
def initialize_vector_store():
    result = vector_store.initialize_schema_embeddings()
    return {"message": result}