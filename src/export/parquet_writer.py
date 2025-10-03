class ParquetWriter:
    def write_to_parquet(self, data, file_path):
        import pandas as pd
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        
        # Write the DataFrame to a Parquet file
        df.to_parquet(file_path, index=False)