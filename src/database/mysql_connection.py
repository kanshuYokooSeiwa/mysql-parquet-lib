from typing import Optional
import mysql.connector
from mysql.connector import MySQLConnection as MySQLConn
from config.database_config import DatabaseConfig

class MySQLConnection:
    def __init__(self, config: DatabaseConfig) -> None:
        self.config: DatabaseConfig = config
        self.connection: Optional[MySQLConn] = None

    def connect(self) -> MySQLConn:
        self.connection = mysql.connector.connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database
        )
        return self.connection

    def close(self) -> None:
        if self.connection:
            self.connection.close()