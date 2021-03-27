import io
import os
import string
from logging import Logger
from math import sqrt

import matplotlib.pyplot as plt
from pandas._typing import Level
from pandas.plotting._matplotlib import lag_plot
from pyspark.sql.functions import col
from pyspark.shell import spark
from pyspark.sql import SQLContext, SparkSession

from statsmodels.tsa.arima_model import ARIMA, ARIMA_DEPRECATION_WARN

from sklearn.metrics import mean_squared_error
import numpy as np
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext, SparkFiles
from pyspark.sql import HiveContext
import pyspark.sql.functions as sqf

def int_or_float(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


spark = SparkSession.builder.master('local[*]').appName('ICULux').config("spark.files.overwrite", "true")\
    .config("spark.worker.cleanup.enabled","true").getOrCreate()
sc = spark.sparkContext
url = "https://physionet.org/files/mimicdb/1.0.0/055/05500001.txt"
sc.addFile(url)


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


readfrmfile = spark.read.csv("temp.txt", header="false", schema=schema, sep='\\t')
readfrmfile = readfrmfile.filter(readfrmfile.Name == "SpO2")

df = readfrmfile.toPandas()
train_data, test_data = df[0:int(len(df)*0.5)], df[int(len(df)*0.5):]
training_data = train_data['val1'].values
training_data = np.array(training_data)
training_data = training_data.astype(int)
test_data = test_data['val1'].values
test_data = np.array(test_data)
test_data = test_data.astype(int)
print(training_data)
history = [x for x in training_data]
model_predictions = []
N_test_observations = len(test_data)
for time_point in range(N_test_observations):
    model = ARIMA(history, order=(4,1,1))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)
    true_test_value = test_data[time_point]
    history.append(true_test_value)
    print('predicted=%f, expected=%f' % (yhat, true_test_value))
    model_fit.save("sp02.pkl")

rmse = sqrt(mean_squared_error(test_data, model_predictions))
print('Test RMSE: %.3f' % rmse)

test_set_range = df[int(len(df)*0.5):].index
plt.plot(test_set_range, model_predictions, color='blue', marker='o', linestyle='dashed',label='Predicted Price')
plt.plot(test_set_range, test_data, color='red', label='Actual Price')
plt.legend()
plt.show()
os.remove("tmp/temp.txt")