class QueryExecutor:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results