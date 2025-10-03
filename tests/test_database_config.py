import unittest
from typing import Dict

from config.database_config import DatabaseConfig


class TestDatabaseConfig(unittest.TestCase):
    
    def test_init_with_all_parameters(self) -> None:
        """Test DatabaseConfig initialization with all parameters."""
        host: str = "localhost"
        user: str = "testuser" 
        password: str = "testpass"
        database: str = "testdb"
        
        config: DatabaseConfig = DatabaseConfig(host, user, password, database)
        
        self.assertEqual(config.host, host)
        self.assertEqual(config.user, user)
        self.assertEqual(config.password, password)
        self.assertEqual(config.database, database)
    
    def test_init_with_default_parameters(self) -> None:
        """Test DatabaseConfig initialization with default parameters."""
        config: DatabaseConfig = DatabaseConfig()
        
        self.assertEqual(config.host, "")
        self.assertEqual(config.user, "")
        self.assertEqual(config.password, "")
        self.assertEqual(config.database, "")
    
    def test_init_with_partial_parameters(self) -> None:
        """Test DatabaseConfig initialization with partial parameters."""
        config: DatabaseConfig = DatabaseConfig(host="localhost", database="testdb")
        
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.user, "")
        self.assertEqual(config.password, "")
        self.assertEqual(config.database, "testdb")
    
    def test_to_dict(self) -> None:
        """Test to_dict method returns correct dictionary."""
        host: str = "localhost"
        user: str = "testuser"
        password: str = "testpass"
        database: str = "testdb"
        
        config: DatabaseConfig = DatabaseConfig(host, user, password, database)
        result_dict: Dict[str, str] = config.to_dict()
        
        expected_dict: Dict[str, str] = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        self.assertEqual(result_dict, expected_dict)
    
    def test_to_dict_with_defaults(self) -> None:
        """Test to_dict method with default values."""
        config: DatabaseConfig = DatabaseConfig()
        result_dict: Dict[str, str] = config.to_dict()
        
        expected_dict: Dict[str, str] = {
            'host': "",
            'user': "",
            'password': "",
            'database': ""
        }
        
        self.assertEqual(result_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()