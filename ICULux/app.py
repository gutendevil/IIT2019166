from flask import Flask,render_template,flash,redirect,request,session,abort
import os
app = Flask(__name__)

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
               return render_template('login.html')
          else:
               return render_template('index.html')
    
if __name__ == "__main__":
     app.secret_key = os.urandom(12)
     app.run(debug=True)
