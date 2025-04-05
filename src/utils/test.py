import pandas as pd
import os

file_path = os.path.join(os.getcwd(), 'data', 'processed', 'cleaned_logs.csv')
df = pd.read_csv(file_path)
print(df.columns)