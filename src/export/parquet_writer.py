from typing import List, Tuple, Any
import pandas as pd

class ParquetWriter:
    def __init__(self) -> None:
        pass
    
    def write_to_parquet(self, data: List[Tuple[Any, ...]], file_path: str) -> None:
        # Convert the data to a DataFrame
        df: pd.DataFrame = pd.DataFrame(data)
        
        # Write the DataFrame to a Parquet file
        df.to_parquet(file_path, index=False)