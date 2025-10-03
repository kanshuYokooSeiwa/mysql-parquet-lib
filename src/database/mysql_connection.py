class MySQLConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        import mysql.connector
        self.connection = mysql.connector.connect(
            host=self.config.get('host', ''),
            user=self.config.get('user', ''),
            password=self.config.get('password', ''),
            database=self.config.get('database', '')
        )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()