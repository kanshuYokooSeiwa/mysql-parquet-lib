import unittest
import os
from typing import List, Tuple, Any, Optional
from unittest import skipIf
import mysql.connector
from mysql.connector import Error

from src.database.mysql_connection import MySQLConnection
from src.query.query_executor import QueryExecutor
from config.database_config import DatabaseConfig


class TestQueryExecutorRealDB(unittest.TestCase):
    """
    Integration tests for QueryExecutor using real MySQL database.
    
    Prerequisites:
    1. MySQL server running locally
    2. Database 'testdb' exists
    3. User 'testuser' with password 'testpass' has access to 'testdb'
    4. Test tables 'users' and 'orders' exist with sample data
    
    To set up the test database, run the SQL commands provided in README.md
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test database configuration and check connectivity."""
        cls.config: DatabaseConfig = DatabaseConfig(
            host="localhost",
            user="testuser",
            password="testpass",
            database="testdb"
        )
        
        # Check if we can connect to the database
        cls.db_available: bool = cls._check_database_availability()
        
        if cls.db_available:
            cls.mysql_connection: MySQLConnection = MySQLConnection(cls.config)
            cls.connection = cls.mysql_connection.connect()
            cls.query_executor: QueryExecutor = QueryExecutor(cls.connection)
            
            # Verify test tables exist
            cls._verify_test_tables()
    
    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up database connection."""
        if hasattr(cls, 'mysql_connection') and cls.mysql_connection:
            cls.mysql_connection.close()
    
    @classmethod
    def _check_database_availability(cls) -> bool:
        """Check if the test database is available."""
        try:
            test_connection = mysql.connector.connect(
                host=cls.config.host,
                user=cls.config.user,
                password=cls.config.password,
                database=cls.config.database
            )
            test_connection.close()
            return True
        except Error as e:
            print(f"Database not available: {e}")
            return False
    
    @classmethod
    def _verify_test_tables(cls) -> None:
        """Verify that required test tables exist."""
        required_tables: List[str] = ['users', 'orders']
        
        try:
            cursor = cls.connection.cursor()
            cursor.execute("SHOW TABLES")
            existing_tables: List[str] = [table[0] for table in cursor.fetchall()]
            cursor.close()
            
            missing_tables: List[str] = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                raise unittest.SkipTest(f"Missing required test tables: {missing_tables}")
                
        except Error as e:
            raise unittest.SkipTest(f"Could not verify test tables: {e}")
    
    def setUp(self) -> None:
        """Set up for each test method."""
        if not self.db_available:
            self.skipTest("Database not available")
    
    def test_execute_simple_select_query(self) -> None:
        """Test executing a simple SELECT query."""
        query: str = "SELECT id, name, email FROM users ORDER BY id LIMIT 2"
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        # Verify results structure
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertEqual(len(results), 2)  # LIMIT 2
        
        # Verify each row has 3 columns
        for row in results:
            self.assertEqual(len(row), 3)
            self.assertIsInstance(row[0], int)  # id
            self.assertIsInstance(row[1], str)  # name
            self.assertIsInstance(row[2], str)  # email
    
    def test_execute_query_with_where_clause(self) -> None:
        """Test executing a query with WHERE clause."""
        query: str = "SELECT name, age FROM users WHERE age > 25 ORDER BY age"
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Verify age filtering worked
        for row in results:
            age: int = row[1]
            self.assertGreater(age, 25)
    
    def test_execute_join_query(self) -> None:
        """Test executing a JOIN query."""
        query: str = """
        SELECT u.name, u.email, o.product_name, o.quantity, o.price
        FROM users u
        JOIN orders o ON u.id = o.user_id
        ORDER BY u.name, o.product_name
        """
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Verify join structure
        for row in results:
            self.assertEqual(len(row), 5)  # 5 selected columns
            self.assertIsInstance(row[0], str)  # name
            self.assertIsInstance(row[1], str)  # email
            self.assertIsInstance(row[2], str)  # product_name
            self.assertIsInstance(row[3], int)  # quantity
    
    def test_execute_aggregate_query(self) -> None:
        """Test executing an aggregate query."""
        query: str = """
        SELECT COUNT(*) as user_count, AVG(age) as avg_age, MIN(age) as min_age, MAX(age) as max_age
        FROM users
        """
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)  # Aggregate should return 1 row
        
        row: Tuple[Any, ...] = results[0]
        self.assertEqual(len(row), 4)  # 4 aggregate columns
        
        user_count: int = row[0]
        avg_age: float = row[1]
        min_age: int = row[2]
        max_age: int = row[3]
        
        self.assertGreater(user_count, 0)
        self.assertGreater(avg_age, 0)
        self.assertGreaterEqual(max_age, min_age)
    
    def test_execute_empty_result_query(self) -> None:
        """Test executing a query that returns no results."""
        query: str = "SELECT * FROM users WHERE age > 100"
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
    
    def test_execute_invalid_query(self) -> None:
        """Test executing an invalid SQL query."""
        query: str = "SELECT * FROM non_existent_table"
        
        with self.assertRaises(Exception):
            self.query_executor.execute_query(query)
    
    def test_execute_query_with_special_characters(self) -> None:
        """Test executing a query with special characters in data."""
        # First, insert a test record with special characters
        setup_query: str = """
        INSERT IGNORE INTO users (name, email, age) 
        VALUES ('Test User & Co.', 'test+special@example.com', 30)
        """
        
        try:
            # Setup test data
            cursor = self.connection.cursor()
            cursor.execute(setup_query)
            self.connection.commit()
            cursor.close()
            
            # Test the query
            query: str = "SELECT name, email FROM users WHERE name LIKE '%&%'"
            results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
            
            self.assertIsInstance(results, list)
            if len(results) > 0:
                self.assertIn('&', results[0][0])  # name should contain &
                
        except Exception as e:
            self.fail(f"Query with special characters failed: {e}")
    
    def test_execute_query_with_null_values(self) -> None:
        """Test executing a query that may return NULL values."""
        # Insert a user with a NULL age
        setup_query: str = """
        INSERT IGNORE INTO users (name, email, age) 
        VALUES ('Test User NULL', 'test_null@example.com', NULL)
        """
        
        try:
            # Setup test data
            cursor = self.connection.cursor()
            cursor.execute(setup_query)
            self.connection.commit()
            cursor.close()
            
            # Test the query
            query: str = "SELECT name, email, age FROM users WHERE name = 'Test User NULL'"
            results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
            
            self.assertIsInstance(results, list)
            if len(results) > 0:
                self.assertIsNone(results[0][2])  # age should be None
                
        except Exception as e:
            self.fail(f"Query with NULL values failed: {e}")
    
    def test_execute_order_by_query(self) -> None:
        """Test executing a query with ORDER BY clause."""
        query: str = "SELECT name, age FROM users ORDER BY age DESC"
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Verify ordering (should be descending by age)
        previous_age: Optional[int] = None
        for row in results:
            current_age: Optional[int] = row[1]
            if previous_age is not None and current_age is not None:
                self.assertGreaterEqual(previous_age, current_age)
            previous_age = current_age
    
    def test_execute_group_by_query(self) -> None:
        """Test executing a query with GROUP BY clause."""
        query: str = """
        SELECT u.name, COUNT(o.id) as order_count, SUM(o.price) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.name
        ORDER BY u.name
        """
        
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Verify group by structure
        for row in results:
            self.assertEqual(len(row), 3)  # name, order_count, total_spent
            self.assertIsInstance(row[0], str)  # name
            self.assertIsInstance(row[1], int)  # order_count
            # total_spent can be None (for users with no orders) or Decimal
    
    def test_execute_limit_offset_query(self) -> None:
        """Test executing a query with LIMIT and OFFSET."""
        # First, get total count
        count_query: str = "SELECT COUNT(*) FROM users"
        count_results: List[Tuple[Any, ...]] = self.query_executor.execute_query(count_query)
        total_count: int = count_results[0][0]
        
        # Test with LIMIT
        query: str = "SELECT id, name FROM users ORDER BY id LIMIT 2"
        results: List[Tuple[Any, ...]] = self.query_executor.execute_query(query)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 2)
        
        # Test with LIMIT and OFFSET
        if total_count > 2:
            offset_query: str = "SELECT id, name FROM users ORDER BY id LIMIT 2 OFFSET 1"
            offset_results: List[Tuple[Any, ...]] = self.query_executor.execute_query(offset_query)
            
            self.assertIsInstance(offset_results, list)
            if len(results) > 1 and len(offset_results) > 0:
                # First result from offset query should not match first result from regular query
                self.assertNotEqual(results[0][0], offset_results[0][0])


if __name__ == '__main__':
    unittest.main()