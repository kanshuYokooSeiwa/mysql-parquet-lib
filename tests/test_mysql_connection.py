import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
import mysql.connector
from mysql.connector import MySQLConnection as MySQLConn

from src.database.mysql_connection import MySQLConnection
from config.database_config import DatabaseConfig


class TestMySQLConnection(unittest.TestCase):
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.config: DatabaseConfig = DatabaseConfig(
            host="localhost",
            user="testuser",
            password="testpass",
            database="testdb"
        )
        self.mysql_connection: MySQLConnection = MySQLConnection(self.config)
    
    @patch('src.database.mysql_connection.mysql.connector.connect')
    def test_connect_success(self, mock_connect: Mock) -> None:
        """Test successful database connection."""
        mock_conn: Mock = Mock(spec=MySQLConn)
        mock_connect.return_value = mock_conn
        
        result: MySQLConn = self.mysql_connection.connect()
        
        mock_connect.assert_called_once_with(
            host="localhost",
            user="testuser",
            password="testpass",
            database="testdb"
        )
        self.assertEqual(result, mock_conn)
        self.assertEqual(self.mysql_connection.connection, mock_conn)
    
    @patch('src.database.mysql_connection.mysql.connector.connect')
    def test_connect_failure(self, mock_connect: Mock) -> None:
        """Test database connection failure."""
        mock_connect.side_effect = mysql.connector.Error("Connection failed")
        
        with self.assertRaises(mysql.connector.Error):
            self.mysql_connection.connect()
    
    def test_close_with_connection(self) -> None:
        """Test closing an existing connection."""
        mock_connection: Mock = Mock(spec=MySQLConn)
        self.mysql_connection.connection = mock_connection
        
        self.mysql_connection.close()
        
        mock_connection.close.assert_called_once()
    
    def test_close_without_connection(self) -> None:
        """Test closing when no connection exists."""
        self.mysql_connection.connection = None
        
        # Should not raise any exception
        self.mysql_connection.close()


if __name__ == '__main__':
    unittest.main()