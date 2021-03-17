import time

import flask
import mysql
from flask import Flask, render_template, flash, redirect, request, session, abort, jsonify, url_for, Response, \
     stream_with_context
from flaskext.mysql import MySQL
from mysql import connector
from pyspark.sql import SQLContext, SparkSession
import os
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext, SparkFiles
from pyspark.sql.functions import col
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


import re
import os
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'icu'
patientdata = None


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
     return render_template('about.html')
@app.route("/contact")
def contact():
     return render_template('contact.html')
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
     if request.method=='POST':
          if request.form.get('password') == 'iculux' and request.form.get('username') == 'admin':
               return render_template('find_patient.html')
          else:
               return render_template('index.html')
@app.route('/find_patient', methods=['POST','GET'])
def find_patient():
     msg = ""
     if(request.method == 'POST'):
          print(request.form['pid'])
          if 'pid' in request.form:
               pid = request.form['pid']
               if re.match(r'[A-Za-z]+', pid):
                    msg += "Patient id should be numeric in value."
                    return render_template("find_patient.html", msg=msg)
               elif re.match(r'[0-9]+', pid):
                    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='icu')
                    cursor = cnx.cursor()
                    cursor.execute('SELECT * FROM Patient_Information WHERE pid = %s', (pid,))
                    details = cursor.fetchall()
                    cursor.close()
                    global patientdata
                    patientdata = details
                    return redirect(url_for('data'))
               else:
                    msg += "Please enter valid input."
                    return render_template("find_patient.html", msg=msg)
          else:
               msg += "Please fill the form."
               return render_template("find_patient.html", msg=msg)

def temp():
     return render_template("data.html", data=patientdata)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    #rv.enable_buffering(5)
    return rv

@app.route('/data', methods=['POST','GET'])
def data():
     temp()
     print("hello2\n")

     spark = SparkSession.builder.master('local[*]').appName('ICULux').config("spark.files.overwrite", "true") \
         .config("spark.worker.cleanup.enabled", "true").getOrCreate()
     sc = spark.sparkContext
     url = "https://physionet.org/files/mimicdb/1.0.0/055/05500001.txt"
     sc.addFile(url)

    # first get all lines from file
     with open(SparkFiles.get("05500001.txt"), 'r') as f:
          lines = f.readlines()

    # remove spaces
     lines = [line.replace(' ', '') for line in lines]

    # finally, write lines in the file
     with open("temp.txt", 'w') as f:
          f.writelines(lines)



     schema = StructType([
          StructField("Name", StringType(), True),
          StructField("val1", StringType(), True),
          StructField("val2", StringType(), True),
          StructField("val3", StringType(), True)])

     readfrmfile = spark.read.csv("temp.txt", header="false", schema=schema, sep='\\t')

     readfrmfile = readfrmfile.filter(col('Name').startswith('[') == False)
     rows = readfrmfile.collect()

     os.remove("temp.txt")

     def inner():
          # simulate a long process to watch
          for i in rows:
               name = i[0]
               val1 = i[1]
               val2 = i[2]
               val3 = i[3]
               time.sleep(1)
               # this value should be inserted into an HTML template
               if (val3 != None and val2 != None):
                    yield str(name) + " " + str(val1) + " " + str(val2) + " " + str(val3) + '<br/>\n'
               else:
                    yield str(name) + " " + str(val1) + '<br/>\n'
     rows = inner()
     return Response(inner())

if __name__ == "__main__":
     app.secret_key = os.urandom(12)
     app.run(debug=True)
