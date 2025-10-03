# MySQL to Parquet Utility Library

This library provides a simple interface to connect to a MySQL database, execute SQL queries, and save the results in Apache Parquet format.

## Features

- Connect to a MySQL database using configurable settings.
- Execute SQL queries and retrieve results.
- Export query results to Apache Parquet format for efficient storage and processing.

## Prerequisites

### MySQL Server
This library requires access to a MySQL database server. **MySQL must be installed on your local computer if you plan to run tests** or develop with this library.

**Installation Options:**
- **macOS**: Install via Homebrew: `brew install mysql`
- **Ubuntu/Debian**: `sudo apt-get install mysql-server`
- **Windows**: Download from [MySQL official website](https://dev.mysql.com/downloads/mysql/)
- **Docker**: `docker run --name mysql-server -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0`

**Important Database Connection Requirements:**
- **Connection Information**: You must have valid connection credentials (host, user, password, database name)
- **Network Access**: Ensure your computer can connect to the target MySQL server
- **Firewall Settings**: Verify that the MySQL server allows connections from your computer's IP address
- **Database Permissions**: The user account must have appropriate privileges (SELECT for queries, CREATE/INSERT for tests)

**Before using this library**, test your database connection using a MySQL client:
```bash
mysql -h your_host -u your_username -p your_database
```

### Python Dependencies
To install the required Python dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Connecting to MySQL

To connect to a MySQL database, create an instance of the `MySQLConnection` class from the `mysql_connection` module and provide the necessary configuration.

### Executing Queries

Use the `QueryExecutor` class from the `query_executor` module to execute your SQL queries. Pass the SQL query as a parameter to the `execute_query` method.

### Exporting to Parquet

To save the results of your query in Parquet format, use the `ParquetWriter` class from the `parquet_writer` module. Call the `write_to_parquet` method with the query results.

## Example

```python
from src.database.mysql_connection import MySQLConnection
from src.query.query_executor import QueryExecutor
from src.export.parquet_writer import ParquetWriter
from config.database_config import DatabaseConfig

# Create database configuration
config = DatabaseConfig(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Create a MySQL connection
mysql_conn = MySQLConnection(config)
connection = mysql_conn.connect()

# Execute a query
query_executor = QueryExecutor(connection)
results = query_executor.execute_query("SELECT * FROM your_table")

# Write results to Parquet
parquet_writer = ParquetWriter()
parquet_writer.write_to_parquet(results, 'output.parquet')

# Clean up
mysql_conn.close()
```

## Integration Examples

The library includes comprehensive integration examples that demonstrate real-world usage patterns with the test database. These examples show how to connect to MySQL, execute various types of queries, and export results to organized Parquet files.

### Prerequisites for Examples

Before running the integration examples, ensure you have:

1. **MySQL Server**: Running locally with the test database set up (see [Step-by-Step Database Setup](#step-by-step-database-setup))
2. **Test Database**: Database `testdb` with user `testuser` and sample data
3. **Python Dependencies**: All requirements installed (`pip install -r requirements.txt`)

### Basic Integration Example

**File**: `examples/basic_integration_example.py`

**Purpose**: Demonstrates fundamental library usage patterns with simple queries and exports.

**What it does**:
- Connects to the test MySQL database
- Executes simple SELECT queries  
- Exports data to Parquet files in a `parquetFiles/` directory
- Shows proper connection management and error handling

**Usage**:
```bash
# From the project root directory
python examples/basic_integration_example.py
```

**Generated Files**:
- `parquetFiles/users.parquet` - All user records
- `parquetFiles/orders.parquet` - All order records
- `parquetFiles/high_value_customers.parquet` - Users with orders > $100

### Advanced Integration Example

**File**: `examples/advanced_integration_example.py`

**Purpose**: Showcases complex analytics and business intelligence scenarios.

**What it does**:
- Validates database connectivity before processing
- Executes complex analytical queries (JOINs, aggregations, window functions)
- Creates timestamped export directories for organized data management
- Generates comprehensive business analytics reports
- Provides detailed success/failure reporting

**Usage**:
```bash
# From the project root directory
python examples/advanced_integration_example.py
```

**Generated Analytics Files**:
- `user_order_summary.parquet` - Customer purchase behavior analysis
- `product_performance.parquet` - Product sales and revenue metrics
- `age_demographic_analysis.parquet` - Customer demographic insights  
- `high_value_transactions.parquet` - Premium order analysis with rankings
- `customer_lifetime_value.parquet` - Customer segmentation and LTV analysis
- `export_summary.parquet` - Processing metadata and success metrics

### Expected Output Structure

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

### Using the Generated Parquet Files

The exported Parquet files can be analyzed with various tools:

**With Pandas**:
```python
import pandas as pd

# Load exported data
users_df = pd.read_parquet('parquetFiles/users.parquet')
orders_df = pd.read_parquet('parquetFiles/orders.parquet')

# Analyze the data
print(users_df.info())
print(orders_df.describe())
```

**With DuckDB (SQL Analytics)**:
```python
import duckdb

# Query parquet files directly with SQL
conn = duckdb.connect()
result = conn.execute("""
    SELECT * FROM 'parquetFiles/advanced_export_*/user_order_summary.parquet'
    WHERE total_spent > 500
    ORDER BY total_spent DESC
""").fetchall()
```

### Troubleshooting Examples

**Database Connection Issues**:
- Verify MySQL is running: `brew services list | grep mysql`
- Test connection: `mysql -h localhost -u testuser -p testdb`
- Check that test tables exist and have data

**Import Path Issues**:
- Always run examples from the project root directory
- Ensure the project structure is intact

**Permission Errors**:
- Verify `testuser` has proper privileges on `testdb`
- Check that the `parquetFiles/` directory can be created

For detailed examples documentation, see [`examples/README.md`](examples/README.md).

## Running Tests

This project includes comprehensive unit tests with proper typing. 

### Test Database Setup

**Important**: Most tests use mocking and don't require a real database connection. However, if you want to test with a real MySQL database, you'll need:

1. **MySQL Server Running**: Ensure MySQL is installed and running on your local machine
2. **Test Database**: Create a test database (optional, as tests use mocked connections)
3. **Connection Credentials**: The tests use mock connections with these sample credentials:
   - Host: `localhost`
   - User: `testuser`
   - Password: `testpass`
   - Database: `testdb`

**Note**: The unit tests are designed to work without a real database connection using Python's `unittest.mock` library. They test the code logic and behavior without requiring actual MySQL connectivity.

### Running Tests

To run the tests:

### Run All Tests

```bash
# From the project root directory
python -m pytest tests/ -v
```

### Run Individual Test Files

```bash
# Test MySQL connection
python -m pytest tests/test_mysql_connection.py -v

# Test query executor (mock-based unit tests)
python -m pytest tests/test_query_executor.py -v

# Test query executor with real database (integration tests)
python -m pytest tests/test_query_executor_realDB.py -v

# Test both query executor files
python -m pytest tests/test_query_executor*.py -v

# Test parquet writer
python -m pytest tests/test_parquet_writer.py -v

# Test database config
python -m pytest tests/test_database_config.py -v
```

### Run Tests with Coverage

```bash
# Install coverage if not already installed
pip install coverage pytest

# Run tests with coverage
coverage run -m pytest tests/
coverage report -m
coverage html  # Generate HTML coverage report
```

### Run Tests Using unittest

Alternatively, you can run tests using Python's built-in unittest module:

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run individual test files
python -m unittest tests.test_mysql_connection -v
python -m unittest tests.test_query_executor -v
python -m unittest tests.test_parquet_writer -v
python -m unittest tests.test_database_config -v
```

## Development

### Test Requirements

For development and testing, install additional dependencies:

```bash
pip install pytest coverage
```

### Setting Up a Test Database (Optional)

If you want to test with a real MySQL database instead of mocked connections:

1. **Install MySQL** on your local machine (see Prerequisites section)
2. **Start MySQL service**:
   ```bash
   # macOS (if installed via Homebrew)
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   
   # Or using Docker
   docker run --name test-mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0
   ```
3. **Create a test database and user**:

#### Step-by-Step Database Setup

**Step 1: Connect to MySQL as root**
```bash
mysql -u root -p
```
Enter your root password when prompted.

**Step 2: Create the database testdb**
```sql
CREATE DATABASE testdb;
```
This creates a new database named `testdb` for testing purposes.

**Step 3: Create the user testuser with the password testpass**
```sql
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass';
```
This command creates a user that can only connect from your local machine (localhost).

**Step 4: Grant all privileges on testdb to testuser**
```sql
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
```
This command gives your new user full control (create, read, update, delete, etc.) over only the testdb database.

**Step 5: Apply the changes**
```sql
FLUSH PRIVILEGES;
```
This command reloads the permission tables to ensure your new user's privileges are active immediately.

**Step 6: Exit MySQL**
```sql
EXIT;
```

**Step 7: Test the new connection**
```bash
mysql -h localhost -u testuser -p testdb
```
Enter `testpass` when prompted. If successful, you should be connected to the testdb database as testuser.

**Step 8: Create test tables and insert sample data**
```sql
-- Ensure you're using the testdb database
USE testdb;

-- Create test tables
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product_name VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 1,
    price DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert test data
INSERT INTO users (name, email, age) VALUES
('John Doe', 'john@example.com', 30),
('Jane Smith', 'jane@example.com', 25),
('Bob Johnson', 'bob@example.com', 35),
('Alice Brown', 'alice@example.com', 28);

INSERT INTO orders (user_id, product_name, quantity, price) VALUES
(1, 'Laptop', 1, 999.99),
(1, 'Mouse', 2, 25.50),
(2, 'Keyboard', 1, 75.00),
(3, 'Monitor', 1, 299.99),
(4, 'Headphones', 1, 150.00);
```

**Step 9: Exit MySQL**
```sql
EXIT;
```

**Note**: The current unit tests use mocking and don't require a real database connection. This setup is only needed if you plan to write integration tests or test with real data. The real database integration tests are available in `test_query_executor_realDB.py`.

### Code Quality

All code follows strict typing conventions:
- Function parameters have type hints
- Return types are annotated
- Variables within functions are explicitly typed
- All necessary types are imported from the `typing` module

## Contributing

Contributions are welcome! Please ensure:
1. All new code includes proper type annotations
2. Unit tests are provided for new functionality
3. Tests pass before submitting pull requests
4. Follow the existing code style and typing conventions

## License

This project is licensed under the MIT License. See the LICENSE file for more details.