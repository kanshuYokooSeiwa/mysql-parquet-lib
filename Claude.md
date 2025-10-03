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
- [ ] Unit tests with type hints
- [ ] Integration examples
- [ ] Error handling enhancement

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