import pandas as pd
df = pd.read_csv("/opt/airflow/scripts/data/raw.csv")

df = df.dropna()

df.to_csv("/opt/airflow/scripts/data/clean/clean.csv", index=False)

print("Cleaned data saved to data/clean/clean.csv")
