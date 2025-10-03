# Integration Examples

This directory contains practical examples demonstrating how to use the MySQL to Parquet utility library with real database connections and data export scenarios.

## Prerequisites

Before running these examples, ensure you have:

1. **MySQL Server**: Running locally or accessible remotely
2. **Test Database**: Set up according to the main README.md instructions:
   - Database: `testdb`
   - User: `testuser` 
   - Password: `testpass`
   - Tables: `users` and `orders` with sample data
3. **Python Dependencies**: Install via `pip install -r requirements.txt`

## Examples Overview

### 1. Basic Integration Example (`basic_integration_example.py`)

**Purpose**: Demonstrates fundamental library usage patterns

**What it does**:
- Connects to the test MySQL database
- Executes simple SELECT queries
- Exports data to Parquet files in a `parquetFiles/` directory
- Shows proper connection management and error handling

**Exports created**:
- `users.parquet` - All user records
- `orders.parquet` - All order records  
- `high_value_customers.parquet` - Users with orders > $100

**Usage**:
```bash
cd /path/to/mysql-parquet-lib
python examples/basic_integration_example.py
```

### 2. Advanced Integration Example (`advanced_integration_example.py`)

**Purpose**: Showcases complex analytics and business intelligence scenarios

**What it does**:
- Validates database connectivity before processing
- Executes complex analytical queries (JOINs, aggregations, window functions)
- Creates timestamped export directories
- Generates comprehensive business analytics reports
- Provides detailed success/failure reporting

**Analytics exports created**:
- `user_order_summary.parquet` - Customer purchase behavior analysis
- `product_performance.parquet` - Product sales and revenue metrics
- `age_demographic_analysis.parquet` - Customer demographic insights
- `high_value_transactions.parquet` - Premium order analysis with rankings
- `customer_lifetime_value.parquet` - Customer segmentation and LTV analysis
- `export_summary.parquet` - Processing metadata and success metrics

**Usage**:
```bash
cd /path/to/mysql-parquet-lib
python examples/advanced_integration_example.py
```

## Expected Output Structure

After running the examples, you'll have the following directory structure:

```
mysql-parquet-lib/
├── parquetFiles/
│   ├── users.parquet                    # Basic example output
│   ├── orders.parquet
│   ├── high_value_customers.parquet
│   └── advanced_export_YYYYMMDD_HHMMSS/ # Advanced example output
│       ├── user_order_summary.parquet
│       ├── product_performance.parquet
│       ├── age_demographic_analysis.parquet
│       ├── high_value_transactions.parquet
│       ├── customer_lifetime_value.parquet
│       └── export_summary.parquet
```

## Using the Exported Data

The generated Parquet files can be used with various data analysis tools:

### With Pandas
```python
import pandas as pd

# Load exported data
users_df = pd.read_parquet('parquetFiles/users.parquet')
orders_df = pd.read_parquet('parquetFiles/orders.parquet')

# Analyze the data
print(users_df.info())
print(orders_df.describe())
```

### With Apache Spark
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MySQLParquetAnalysis").getOrCreate()

# Load parquet files
users_df = spark.read.parquet('parquetFiles/users.parquet')
analytics_df = spark.read.parquet('parquetFiles/advanced_export_*/user_order_summary.parquet')

users_df.show()
analytics_df.show()
```

### With DuckDB (SQL Analytics)
```python
import duckdb

# Query parquet files directly with SQL
conn = duckdb.connect()
result = conn.execute("""
    SELECT * FROM 'parquetFiles/user_order_summary.parquet'
    WHERE total_spent > 500
    ORDER BY total_spent DESC
""").fetchall()

print(result)
```

## Troubleshooting

### Common Issues

**Database Connection Errors**:
- Verify MySQL is running: `brew services list | grep mysql`
- Test connection: `mysql -h localhost -u testuser -p testdb`
- Check firewall settings and port 3306 accessibility

**Missing Tables**:
- Run the SQL commands from the main README.md to create test tables
- Verify tables exist: `SHOW TABLES;` in MySQL

**Permission Errors**:
- Ensure `testuser` has proper privileges on `testdb`
- Grant permissions: `GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';`

**Import Errors**:
- Run examples from the project root directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Getting Help

If you encounter issues:

1. Check the main README.md for detailed setup instructions
2. Verify your database setup matches the prerequisites exactly
3. Run the unit tests to ensure the library is working: `python -m pytest tests/ -v`
4. Check that your MySQL version is compatible (MySQL 5.7+ recommended)

## Next Steps

After running these examples successfully:

1. **Modify queries**: Edit the SQL queries to match your actual data needs
2. **Automate exports**: Use cron/scheduler to run exports periodically  
3. **Build dashboards**: Connect BI tools like Tableau/PowerBI to the parquet files
4. **Data pipelines**: Integrate into larger ETL/ELT workflows
5. **Cloud deployment**: Upload parquet files to cloud storage (S3, GCS, etc.)

## File Details

- **Type Safety**: All examples follow strict Python typing conventions
- **Error Handling**: Comprehensive exception handling and validation
- **Resource Management**: Proper database connection cleanup
- **Logging**: Detailed progress reporting and success metrics
- **Modularity**: Reusable functions for common operations