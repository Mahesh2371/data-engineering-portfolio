from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

df = spark.read.csv("data/raw.csv", header=True)
df.dropna().write.mode("overwrite").parquet("data/clean/")
