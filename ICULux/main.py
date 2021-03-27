import io
import os
import string
from logging import Logger

import numpy
from pandas._typing import Level
from pyspark.sql.functions import col
from pyspark.shell import spark
from pyspark.sql import SQLContext, SparkSession
import pandas
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext, SparkFiles
from pyspark.sql import HiveContext, window
import pyspark.sql.functions as sqf
from pyspark.streaming import StreamingContext

spark = SparkSession.builder.master('local[*]').appName('ICULux').config("spark.files.overwrite", "true")\
    .config("spark.worker.cleanup.enabled","true").getOrCreate()
sc = spark.sparkContext
ssc = StreamingContext(sc, 1)
conf = SparkConf().setMaster("local[2]").setAppName("NetworkWordCount")

url = "https://physionet.org/files/mimicdb/1.0.0/055/05500001.txt"
sc.addFile(url)

def process_stream(df, spark):
        df.show()


# first get all lines from file
with open(SparkFiles.get("05500001.txt"), 'r') as f:
   lines = f.readlines()

# remove spaces
lines = [line.replace(' ', '') for line in lines]

# finally, write lines in the file
with open("tmp/temp.txt", 'w') as f:
    f.writelines(lines)


schema = StructType([
    StructField("Name",StringType(),True),
    StructField("val1",StringType(),True),
    StructField("val2",StringType(),True),
    StructField("val3", StringType(), True)])


readfrmfile = spark.read.csv("tmp/temp.txt", header="false", schema=schema, sep='\\t')

readfrmfile = readfrmfile.filter((col('Name').startswith('[') == False) & (col('Name') != "INOP")
                                 & (col('Name') != "ALARM"))
distinct_rows = readfrmfile.select(readfrmfile.Name).distinct().collect()
distinct_rows = [r.Name for r in distinct_rows]
print(distinct_rows)
readfrmfile = readfrmfile.toPandas()
df_split = numpy.array_split(readfrmfile, 10)
for i in df_split:
    print(i)
os.remove("tmp/temp.txt")




