## Important imports ##
import MySQLdb
from flask import Flask, request, Response ,jsonify
import json

##neccesary code##
app = Flask(__name__)

## render 'homepage.html' when 127
@app.route("/")
def hello():
    return render_template('homepage.html')
 
@app.route("/login", methods = ['POST'])
def login():
	#res = request.get_json()
	#get the username
	password = request.form['password']
	policeId = request.form['policeId']
	
	db = MySQLdb.connect("localhost","root","","hackathon")
	cursor = db.cursor()

	cursor.execute("SELECT * from policedetails where policeId='"+policeId+"' and password='"+password+"'")
	pwd = cursor.fetchone()

	if (pwd):

		db.close()
		return "Success"
		#return jsonify({"status":"Success"})
	else:
		db.close()
		return "Failed"
		#return jsonify({"status":"Failed"})

## To run the Flask##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)