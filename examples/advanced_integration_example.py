#!/usr/bin/env python3
"""
Advanced Integration Example: Complex MySQL Queries to Parquet Export

This example demonstrates advanced usage patterns:
1. Complex JOIN operations
2. Aggregate queries with GROUP BY
3. Data analysis queries
4. Multiple export formats in organized structure
5. Error handling and validation

Prerequisites:
- MySQL server running locally
- Test database 'testdb' with user 'testuser' set up (see README.md)
- Test tables 'users' and 'orders' with sample data

Usage:
    python examples/advanced_integration_example.py
"""

import os
import sys
from typing import List, Tuple, Any, Optional, Dict
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the mysql-parquet-lib components
from src.database.mysql_connection import MySQLConnection
from src.query.query_executor import QueryExecutor
from src.export.parquet_writer import ParquetWriter
from config.database_config import DatabaseConfig


def create_timestamped_directory(base_dir: str = "parquetFiles") -> str:
    """
    Create timestamped output directory for parquet files.
    
    Args:
        base_dir: Base directory name for parquet files
        
    Returns:
        str: Path to created directory
    """
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path: str = os.path.join(os.getcwd(), base_dir, f"advanced_export_{timestamp}")
    Path(output_path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created timestamped output directory: {output_path}")
    return output_path


def validate_database_connection(config: DatabaseConfig) -> bool:
    """
    Validate database connection before proceeding.
    
    Args:
        config: Database configuration
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        mysql_connection: MySQLConnection = MySQLConnection(config)
        connection = mysql_connection.connect()
        
        # Test with a simple query
        query_executor: QueryExecutor = QueryExecutor(connection)
        test_results: List[Tuple[Any, ...]] = query_executor.execute_query("SELECT 1")
        
        mysql_connection.close()
        return len(test_results) == 1
        
    except Exception as e:
        print(f"❌ Database connection validation failed: {e}")
        return False


def export_query_to_parquet(
    query_executor: QueryExecutor,
    parquet_writer: ParquetWriter,
    query: str,
    filename: str,
    output_dir: str,
    description: str
) -> bool:
    """
    Execute a query and export results to parquet file.
    
    Args:
        query_executor: Query executor instance
        parquet_writer: Parquet writer instance
        query: SQL query to execute
        filename: Output filename
        output_dir: Output directory
        description: Description for logging
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"\n   📊 {description}...")
        results: List[Tuple[Any, ...]] = query_executor.execute_query(query)
        
        file_path: str = os.path.join(output_dir, filename)
        parquet_writer.write_to_parquet(results, file_path)
        
        print(f"   ✓ Exported {len(results)} records to: {filename}")
        return True
            
    except Exception as e:
        print(f"   ✗ Error exporting {description}: {e}")
        return False


def main() -> None:
    """
    Advanced integration example with complex queries and analytics.
    """
    print("🚀 Starting Advanced MySQL to Parquet Integration Example")
    print("=" * 60)
    
    # Step 1: Setup and validation
    print("📋 Step 1: Setting up database connection...")
    config: DatabaseConfig = DatabaseConfig(
        host="localhost",
        user="testuser",
        password="testpass",
        database="testdb"
    )
    
    print("🔍 Step 2: Validating database connection...")
    if not validate_database_connection(config):
        print("❌ Database validation failed. Please check your setup.")
        sys.exit(1)
    print("✓ Database connection validated")
    
    # Step 3: Create timestamped output directory
    print("\n📁 Step 3: Creating timestamped output directory...")
    output_dir: str = create_timestamped_directory("parquetFiles")
    
    # Step 4: Main processing
    mysql_connection: Optional[MySQLConnection] = None
    
    try:
        mysql_connection = MySQLConnection(config)
        connection = mysql_connection.connect()
        
        query_executor: QueryExecutor = QueryExecutor(connection)
        parquet_writer: ParquetWriter = ParquetWriter()
        
        print("\n🔍 Step 4: Executing advanced queries and exporting to Parquet...")
        
        # Define complex queries for different analytics scenarios
        queries: Dict[str, Dict[str, str]] = {
            "user_order_summary.parquet": {
                "query": """
                SELECT 
                    u.id as user_id,
                    u.name,
                    u.email,
                    u.age,
                    COUNT(o.id) as total_orders,
                    COALESCE(SUM(o.quantity), 0) as total_items,
                    COALESCE(SUM(o.price), 0.00) as total_spent,
                    COALESCE(AVG(o.price), 0.00) as avg_order_value,
                    MIN(o.order_date) as first_order_date,
                    MAX(o.order_date) as last_order_date
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                GROUP BY u.id, u.name, u.email, u.age
                ORDER BY total_spent DESC
                """,
                "description": "User Order Summary Analytics"
            },
            
            "product_performance.parquet": {
                "query": """
                SELECT 
                    o.product_name,
                    COUNT(*) as order_count,
                    SUM(o.quantity) as total_quantity_sold,
                    SUM(o.price) as total_revenue,
                    AVG(o.price) as avg_price,
                    MIN(o.price) as min_price,
                    MAX(o.price) as max_price,
                    COUNT(DISTINCT o.user_id) as unique_customers
                FROM orders o
                GROUP BY o.product_name
                ORDER BY total_revenue DESC
                """,
                "description": "Product Performance Analytics"
            },
            
            "age_demographic_analysis.parquet": {
                "query": """
                SELECT 
                    CASE 
                        WHEN u.age < 25 THEN 'Under 25'
                        WHEN u.age BETWEEN 25 AND 30 THEN '25-30'
                        WHEN u.age BETWEEN 31 AND 35 THEN '31-35'
                        ELSE 'Over 35'
                    END as age_group,
                    COUNT(DISTINCT u.id) as user_count,
                    COUNT(o.id) as total_orders,
                    COALESCE(AVG(o.price), 0.00) as avg_order_value,
                    COALESCE(SUM(o.price), 0.00) as total_spent
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                WHERE u.age IS NOT NULL
                GROUP BY age_group
                ORDER BY user_count DESC
                """,
                "description": "Age Demographic Analysis"
            },
            
            "high_value_transactions.parquet": {
                "query": """
                SELECT 
                    o.id as order_id,
                    u.name as customer_name,
                    u.email,
                    u.age,
                    o.product_name,
                    o.quantity,
                    o.price,
                    o.order_date,
                    RANK() OVER (ORDER BY o.price DESC) as price_rank
                FROM orders o
                JOIN users u ON o.user_id = u.id
                WHERE o.price > 100.00
                ORDER BY o.price DESC
                """,
                "description": "High-Value Transactions Analysis"
            },
            
            "customer_lifetime_value.parquet": {
                "query": """
                SELECT 
                    u.id as customer_id,
                    u.name,
                    u.email,
                    u.age,
                    COUNT(o.id) as lifetime_orders,
                    SUM(o.quantity) as lifetime_items,
                    SUM(o.price) as lifetime_value,
                    DATEDIFF(MAX(o.order_date), MIN(o.order_date)) as customer_lifespan_days,
                    CASE 
                        WHEN COUNT(o.id) = 0 THEN 'No Orders'
                        WHEN COUNT(o.id) = 1 THEN 'Single Purchase'
                        WHEN COUNT(o.id) BETWEEN 2 AND 3 THEN 'Occasional'
                        ELSE 'Frequent'
                    END as customer_segment
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                GROUP BY u.id, u.name, u.email, u.age
                HAVING COUNT(o.id) > 0
                ORDER BY lifetime_value DESC
                """,
                "description": "Customer Lifetime Value Analysis"
            }
        }
        
        # Execute each query and export to parquet
        successful_exports: int = 0
        total_queries: int = len(queries)
        
        for filename, query_info in queries.items():
            success: bool = export_query_to_parquet(
                query_executor=query_executor,
                parquet_writer=parquet_writer,
                query=query_info["query"],
                filename=filename,
                output_dir=output_dir,
                description=query_info["description"]
            )
            if success:
                successful_exports += 1
        
        # Generate summary report
        print("\n📊 Step 5: Generating summary report...")
        summary_data: List[Tuple[str, str]] = [
            ("timestamp", datetime.now().isoformat()),
            ("total_queries", str(total_queries)),
            ("successful_exports", str(successful_exports)),
            ("failed_exports", str(total_queries - successful_exports)),
            ("output_directory", output_dir),
            ("success_rate", f"{(successful_exports/total_queries)*100:.1f}%")
        ]
        
        summary_file: str = os.path.join(output_dir, "export_summary.parquet")
        try:
            parquet_writer.write_to_parquet(summary_data, summary_file)
            print(f"   ✓ Generated summary report: export_summary.parquet")
        except Exception as e:
            print(f"   ⚠️  Could not generate summary report: {e}")
        
        # Final summary
        print("\n🎉 Advanced Integration Example Completed!")
        print("=" * 60)
        print(f"📁 Output directory: {output_dir}")
        print(f"📈 Success rate: {successful_exports}/{total_queries} queries exported")
        print("\n📄 Generated Analytics Files:")
        
        # List all generated parquet files with sizes
        for file_name in sorted(os.listdir(output_dir)):
            if file_name.endswith('.parquet'):
                file_path: str = os.path.join(output_dir, file_name)
                file_size: int = os.path.getsize(file_path)
                print(f"   • {file_name:<35} ({file_size:,} bytes)")
        
        print("\n💡 Next Steps:")
        print("   • Load parquet files in pandas, Apache Spark, or other analytics tools")
        print("   • Use these files for business intelligence and reporting")
        print("   • Schedule this script to run periodically for fresh analytics")
        
    except Exception as e:
        print(f"❌ Error during advanced integration example: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        if mysql_connection:
            print("\n🔒 Closing database connection...")
            mysql_connection.close()
            print("✓ Database connection closed")


if __name__ == "__main__":
    main()