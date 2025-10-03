import unittest
from src.database.mysql_connection import MySQLConnection

class TestMySQLConnection(unittest.TestCase):

    def setUp(self):
        self.connection = MySQLConnection()

    def test_connection_establishment(self):
        # Assuming the MySQLConnection class has a method to establish a connection
        self.assertTrue(self.connection.connect(), "Connection should be established successfully.")

    def test_connection_closure(self):
        # Assuming the MySQLConnection class has a method to close the connection
        self.connection.connect()
        self.connection.close()
        self.assertFalse(self.connection.is_connected(), "Connection should be closed successfully.")

if __name__ == '__main__':
    unittest.main()