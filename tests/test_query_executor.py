import unittest
from unittest.mock import Mock, MagicMock
from typing import List, Tuple, Any
from mysql.connector import MySQLConnection

from src.query.query_executor import QueryExecutor


class TestQueryExecutor(unittest.TestCase):
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.mock_connection: Mock = Mock(spec=MySQLConnection)
        self.query_executor: QueryExecutor = QueryExecutor(self.mock_connection)
    
    def test_execute_query_success(self) -> None:
        """Test successful query execution."""
        # Mock cursor and its methods
        mock_cursor: Mock = MagicMock()
        expected_results: List[Tuple[Any, ...]] = [
            (1, 'John', 'Doe'),
            (2, 'Jane', 'Smith'),
            (3, 'Bob', 'Johnson')
        ]
        mock_cursor.fetchall.return_value = expected_results
        self.mock_connection.cursor.return_value = mock_cursor
        
        query: str = "SELECT id, first_name, last_name FROM users"
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        # Verify cursor operations
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query)
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        
        # Verify results
        self.assertEqual(results, expected_results)
    
    def test_execute_query_empty_results(self) -> None:
        """Test query execution with empty results."""
        mock_cursor: Mock = MagicMock()
        expected_results: List[Tuple[Any, ...]] = []
        mock_cursor.fetchall.return_value = expected_results
        self.mock_connection.cursor.return_value = mock_cursor
        
        query: str = "SELECT * FROM empty_table"
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertEqual(results, expected_results)
        mock_cursor.close.assert_called_once()
    
    def test_execute_query_with_exception(self) -> None:
        """Test query execution with database exception."""
        mock_cursor: Mock = MagicMock()
        mock_cursor.execute.side_effect = Exception("SQL syntax error")
        self.mock_connection.cursor.return_value = mock_cursor
        
        query: str = "INVALID SQL QUERY"
        
        with self.assertRaises(Exception):
            self.query_executor.execute_query(query)
        
        # Ensure cursor is still closed even on exception
        mock_cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()