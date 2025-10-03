# Development Process Guidelines with Claude

## Current Project: MySQL to Parquet Utility Library

### Type Safety Standards
Always follow these typing conventions for all Python code:

1. **Function Parameters**: Add type hints to all function parameters
2. **Return Types**: Add return type annotations to all functions
3. **Variable Types**: Explicitly type all variables within functions
4. **Import Types**: Import necessary types from `typing` module

### Example Pattern:
```python
from typing import List, Tuple, Any, Optional
import pandas as pd

class ExampleClass:
    def __init__(self, config: SomeConfigType) -> None:
        self.config: SomeConfigType = config
    
    def process_data(self, data: List[Tuple[Any, ...]], output_path: str) -> bool:
        processed_data: pd.DataFrame = pd.DataFrame(data)
        result: bool = self.save_data(processed_data, output_path)
        return result
```

### Current Architecture
- **Database Connection**: `MySQLConnection` class with `DatabaseConfig` type
- **Query Execution**: `QueryExecutor` class returning `List[Tuple[Any, ...]]`
- **Data Export**: `ParquetWriter` class for converting to Parquet format

### Project Structure Enhanced
```
mysql-parquet-lib/
├── README.md                              # Main project documentation
├── CLAUDE.md                              # Development guidelines
├── requirements.txt                       # Python dependencies
├── setup.py                               # Package configuration
├── config/                               # Configuration modules
│   ├── __init__.py
│   └── database_config.py                # DatabaseConfig class
├── src/                                  # Source code modules
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── mysql_connection.py           # MySQLConnection class
│   ├── export/
│   │   ├── __init__.py
│   │   └── parquet_writer.py             # ParquetWriter class
│   └── query/
│       ├── __init__.py
│       └── query_executor.py             # QueryExecutor class
├── tests/                                # Test suite
│   ├── __init__.py
│   ├── test_database_config.py           # Mock-based unit tests
│   ├── test_mysql_connection.py          # Mock-based unit tests
│   ├── test_query_executor.py            # Mock-based unit tests
│   ├── test_query_executor_realDB.py     # Real database integration tests
│   └── test_parquet_writer.py            # Mock-based unit tests
├── examples/                             # Integration examples ✨ NEW
│   ├── README.md                         # Examples documentation
│   ├── basic_integration_example.py      # Basic usage patterns
│   └── advanced_integration_example.py   # Advanced analytics scenarios
├── parquetFiles/                         # Generated parquet exports ✨ NEW
│   ├── users.parquet                     # Basic example output
│   ├── orders.parquet                    # Basic example output
│   ├── high_value_customers.parquet      # Basic example output
│   └── advanced_export_YYYYMMDD_HHMMSS/  # Timestamped advanced exports
│       ├── user_order_summary.parquet    # Customer behavior analytics
│       ├── product_performance.parquet   # Sales metrics
│       ├── age_demographic_analysis.parquet # Demographics
│       ├── high_value_transactions.parquet # Premium orders
│       ├── customer_lifetime_value.parquet # LTV analysis
│       └── export_summary.parquet        # Processing metadata
└── htmlcov/                              # Coverage reports
    └── (coverage HTML files)
```

### Integration Examples Usage

The project now includes comprehensive integration examples demonstrating real-world usage:

**Basic Integration Example**:
```bash
# Run basic MySQL to Parquet export example
python examples/basic_integration_example.py
```
- Connects to testdb with testuser
- Exports users, orders, and high-value customers to parquetFiles/
- Demonstrates fundamental library usage patterns

**Advanced Integration Example**:
```bash
# Run advanced analytics and business intelligence example  
python examples/advanced_integration_example.py
```
- Executes complex analytical queries (JOINs, aggregations, window functions)
- Creates timestamped export directories
- Generates comprehensive business analytics reports
- Provides detailed success/failure reporting

**Generated Output Structure**:
- Basic exports saved in `parquetFiles/` 
- Advanced exports in timestamped directories: `parquetFiles/advanced_export_YYYYMMDD_HHMMSS/`
- All examples follow strict typing conventions and proper error handling

### Development Status
- [x] Database configuration structure defined
- [x] MySQL connection class with proper typing
- [x] Query executor with type safety
- [x] Parquet writer with type annotations
- [x] Unit tests with type hints
- [x] Integration examples with real database
- [ ] Error handling enhancement
### Prerequisites and Testing Notes
- **MySQL Installation Required**: MySQL must be installed locally to run tests or develop with this library. See README for installation instructions (Homebrew, apt, Docker, etc).
- **Connection Information**: You must have valid credentials (host, user, password, database name) to connect to any MySQL server. For remote servers, ensure your computer is allowed to connect (firewall, network access).
- **Test Database Setup**: Most unit tests use mocking and do not require a real database. If you want to run integration tests, set up a test database and user with appropriate privileges. Example credentials used in tests:
    - Host: `localhost`
    - User: `testuser`
    - Password: `testpass`
    - Database: `testdb`
- **Connection Verification**: Always verify your connection using a MySQL client before using this library:
    ```bash
    mysql -h your_host -u your_username -p your_database
    ```

### Next Steps
1. Create comprehensive unit tests with proper typing
2. Add error handling with custom exception types
3. Implement logging with typed configurations
4. Add connection pooling support
5. Create usage examples with type annotations

### Code Quality Rules
- All variables must have explicit type annotations
- All functions must have return type annotations
- Use meaningful variable names with proper types
- Import all necessary types at the module level
- Follow PEP 8 standards with type hints