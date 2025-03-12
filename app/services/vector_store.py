import chromadb
import json
import os
from dotenv import load_dotenv
from app.db.schema_inspector import get_table_schema, get_table_names
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

load_dotenv()

class VectorStore:
    def __init__(self):
        # Use SentenceTransformer for embeddings
        # Note: Google doesn't currently have a direct integration with ChromaDB
        # So we'll use SentenceTransformer which is a good local alternative
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # Create a persistent client
        self.client = chromadb.PersistentClient("./chroma_db")
        
        # Create or get the collection with the embedding function
        self.collection = self.client.get_or_create_collection(
            name="table_schemas",
            embedding_function=self.embedding_function
        )
        
    def initialize_schema_embeddings(self):
        """Initialize the vector store with table schema information."""
        table_names = get_table_names()
        
        for table_name in table_names:
            schema = get_table_schema(table_name)
            schema_json = json.dumps(schema)
            
            # Add the schema to the collection
            self.collection.add(
                documents=[schema_json],
                metadatas=[{"table_name": table_name}],
                ids=[table_name]
            )
        
        return f"Initialized {len(table_names)} table schemas in vector store"
    
    def find_relevant_tables(self, query, n=1):
        """Find the most relevant tables for a given query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )
        
        relevant_tables = []
        # Check if we have results
        if results["ids"] and len(results["ids"][0]) > 0:
            table_names = results["ids"][0]
            print('################33', table_names)
            table_schemas = [get_table_schema(table) for table in table_names]
            relevant_tables = table_schemas
        
        return relevant_tables

vector_store = VectorStore()