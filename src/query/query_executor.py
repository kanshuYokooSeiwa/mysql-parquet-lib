from typing import List, Tuple, Any
from mysql.connector import MySQLConnection

class QueryExecutor:
    def __init__(self, connection: MySQLConnection) -> None:
        self.connection: MySQLConnection = connection

    def execute_query(self, query: str) -> List[Tuple[Any, ...]]:
        cursor = self.connection.cursor()
        cursor.execute(query)
        results: List[Tuple[Any, ...]] = cursor.fetchall()
        cursor.close()
        return results