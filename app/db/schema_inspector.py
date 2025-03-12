from sqlalchemy import inspect
from .database import engine

def get_table_names():
    """Get all table names from the database."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def get_table_schema(table_name):
    """Get schema for a specific table."""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    primary_keys = inspector.get_pk_constraint(table_name).get('constrained_columns', [])
    foreign_keys = inspector.get_foreign_keys(table_name)
    
    schema = {
        "table_name": table_name,
        "columns": [{"name": column["name"], 
                    "type": str(column["type"]), 
                    "primary_key": column["name"] in primary_keys} 
                    for column in columns],
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys
    }
    
    return schema

def get_all_schemas():
    """Get schemas for all tables."""
    tables = get_table_names()
    all_schemas = {}
    
    for table in tables:
        all_schemas[table] = get_table_schema(table)
    
    return all_schemas
