# MySQL to Parquet Utility Library

This library provides a simple interface to connect to a MySQL database, execute SQL queries, and save the results in Apache Parquet format.

## Features

- Connect to a MySQL database using configurable settings.
- Execute SQL queries and retrieve results.
- Export query results to Apache Parquet format for efficient storage and processing.

## Installation

To install the required dependencies, run:

```
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

# Create a MySQL connection
mysql_conn = MySQLConnection()
connection = mysql_conn.connect()

# Execute a query
query_executor = QueryExecutor()
results = query_executor.execute_query("SELECT * FROM your_table", connection)

# Write results to Parquet
parquet_writer = ParquetWriter()
parquet_writer.write_to_parquet(results, 'output.parquet')
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.