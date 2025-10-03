#!/usr/bin/env python3
"""
Basic Integration Example: MySQL to Parquet Export

This example demonstrates how to:
1. Connect to the test MySQL database
2. Execute simple queries
3. Export results to Parquet files
4. Save files in organized directory structure

Prerequisites:
- MySQL server running locally
- Test database 'testdb' with user 'testuser' set up (see README.md)
- Test tables 'users' and 'orders' with sample data

Usage:
    python examples/basic_integration_example.py
"""

import os
import sys
from typing import List, Tuple, Any, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the mysql-parquet-lib components
from src.database.mysql_connection import MySQLConnection
from src.query.query_executor import QueryExecutor
from src.export.parquet_writer import ParquetWriter
from config.database_config import DatabaseConfig


def create_output_directory(base_dir: str = "parquetFiles") -> str:
    """
    Create output directory for parquet files.
    
    Args:
        base_dir: Base directory name for parquet files
        
    Returns:
        str: Path to created directory
    """
    output_path: str = os.path.join(os.getcwd(), base_dir)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created output directory: {output_path}")
    return output_path


def main() -> None:
    """
    Main integration example demonstrating MySQL to Parquet workflow.
    """
    print("🚀 Starting MySQL to Parquet Integration Example")
    print("=" * 50)
    
    # Step 1: Create database configuration
    print("📋 Step 1: Setting up database connection...")
    config: DatabaseConfig = DatabaseConfig(
        host="localhost",
        user="testuser",
        password="testpass",
        database="testdb"
    )
    print(f"   Database: {config.database}")
    print(f"   Host: {config.host}")
    print(f"   User: {config.user}")
    
    # Step 2: Create output directory
    print("\n📁 Step 2: Creating output directory...")
    output_dir: str = create_output_directory("parquetFiles")
    
    # Step 3: Establish database connection
    print("\n🔌 Step 3: Connecting to MySQL database...")
    mysql_connection: Optional[MySQLConnection] = None
    
    try:
        mysql_connection = MySQLConnection(config)
        connection = mysql_connection.connect()
        print("✓ Successfully connected to MySQL database")
        
        # Step 4: Initialize query executor
        print("\n⚡ Step 4: Initializing query executor...")
        query_executor: QueryExecutor = QueryExecutor(connection)
        print("✓ Query executor ready")
        
        # Step 5: Initialize parquet writer
        print("\n📝 Step 5: Initializing parquet writer...")
        parquet_writer: ParquetWriter = ParquetWriter()
        print("✓ Parquet writer ready")
        
        # Step 6: Execute queries and export to parquet
        print("\n🔍 Step 6: Executing queries and exporting to Parquet...")
        
        # Example 1: Export all users
        print("\n   📊 Example 1: Exporting all users...")
        users_query: str = "SELECT id, name, email, age, created_at FROM users ORDER BY id"
        users_results: List[Tuple[Any, ...]] = query_executor.execute_query(users_query)
        
        users_file: str = os.path.join(output_dir, "users.parquet")
        try:
            parquet_writer.write_to_parquet(users_results, users_file)
            print(f"   ✓ Exported {len(users_results)} users to: {users_file}")
        except Exception as e:
            print(f"   ✗ Failed to export users data: {e}")
        
        # Example 2: Export all orders
        print("\n   📊 Example 2: Exporting all orders...")
        orders_query: str = "SELECT id, user_id, product_name, quantity, price, order_date FROM orders ORDER BY id"
        orders_results: List[Tuple[Any, ...]] = query_executor.execute_query(orders_query)
        
        orders_file: str = os.path.join(output_dir, "orders.parquet")
        try:
            parquet_writer.write_to_parquet(orders_results, orders_file)
            print(f"   ✓ Exported {len(orders_results)} orders to: {orders_file}")
        except Exception as e:
            print(f"   ✗ Failed to export orders data: {e}")
        
        # Example 3: Export users with high-value orders (filtered data)
        print("\n   📊 Example 3: Exporting users with orders > $100...")
        high_value_query: str = """
        SELECT DISTINCT u.id, u.name, u.email, u.age
        FROM users u
        JOIN orders o ON u.id = o.user_id
        WHERE o.price > 100.00
        ORDER BY u.name
        """
        high_value_results: List[Tuple[Any, ...]] = query_executor.execute_query(high_value_query)
        
        high_value_file: str = os.path.join(output_dir, "high_value_customers.parquet")
        try:
            parquet_writer.write_to_parquet(high_value_results, high_value_file)
            print(f"   ✓ Exported {len(high_value_results)} high-value customers to: {high_value_file}")
        except Exception as e:
            print(f"   ✗ Failed to export high-value customers data: {e}")
        
        # Summary
        print("\n🎉 Integration Example Completed Successfully!")
        print("=" * 50)
        print(f"📁 Output directory: {output_dir}")
        print("📄 Generated Parquet files:")
        
        # List generated files
        for file_name in os.listdir(output_dir):
            if file_name.endswith('.parquet'):
                file_path: str = os.path.join(output_dir, file_name)
                file_size: int = os.path.getsize(file_path)
                print(f"   • {file_name} ({file_size} bytes)")
        
    except Exception as e:
        print(f"❌ Error during integration example: {e}")
        return
        
    finally:
        # Step 7: Clean up connections
        if mysql_connection:
            print("\n🔒 Step 7: Closing database connection...")
            mysql_connection.close()
            print("✓ Database connection closed")


if __name__ == "__main__":
    main()