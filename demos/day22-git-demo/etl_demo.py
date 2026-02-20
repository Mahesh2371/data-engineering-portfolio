import pandas as pd
from io import StringIO

def extract_csv(csv_data):
    return pd.read_csv(StringIO(csv_data))
    
def transform_df(df):
    df['country'] = 'India'
    return df

if __name__ == "__main__":
    csv_str = "id,name\n1,Syed"
    df = extract_csv(csv_str)
    transformed_df2 = transform_df(df)
    print("\n",transformed_df2)
