from sqlalchemy import text
from app.db.database import engine

class SQLService:
    def execute_query(self, query):
        """Execute a SQL query and return the results."""
        try:
            with engine.connect() as connection:
                result = connection.execute(text(query))
                # Convert result to list of dictionaries
                columns = result.keys()
                results = [dict(zip(columns, row)) for row in result.fetchall()]
                return {"success": True, "data": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

sql_service = SQLService()
