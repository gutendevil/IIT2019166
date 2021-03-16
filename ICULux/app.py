import mysql
from flask import Flask, render_template, flash, redirect, request, session, abort, jsonify
from flaskext.mysql import MySQL
from mysql import connector

import re
import os
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'icu'



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
     print("hello\n")
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
                    details = cursor.fetchone()
                    cursor.close()
                    return jsonify(details)
               else:
                    msg += "Please enter valid input."
                    return render_template("find_patient.html", msg=msg)
          else:
               msg += "Please fill the form."
               return render_template("find_patient.html", msg=msg)


if __name__ == "__main__":
     app.secret_key = os.urandom(12)
     app.run(debug=True)
