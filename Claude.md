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

### Development Status
- [x] Database configuration structure defined
- [x] MySQL connection class with proper typing
- [x] Query executor with type safety
- [x] Parquet writer with type annotations
- [x] Unit tests with type hints
- [ ] Integration examples
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