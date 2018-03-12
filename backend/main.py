## Important imports ##
from flask import Flask, render_template
import MySQLdb
import json
##neccesary code##
app = Flask(__name__)

## render 'homepage.html' when 127
@app.route("/")
def hello():
    return render_template('homepage.html')
@app.route("/login")
def login():
	#db = MySQLdb.connect("localhost","root","",)
    return render_template('login.html') 
## To run the Flask##
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)