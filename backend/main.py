## Important imports ##

import MySQLdb
from flask import Flask, request, Response ,jsonify, render_template
import json
import numpy as np
import cv2
import os
#from __future__ import print_function
# print('Hello world!', file=sys.stderr)
##neccesary code##
app = Flask(__name__)

## define the location of the upload directory and configure
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''
	renders the homepage
'''
@app.route("/")
def hello():
    return render_template('homepage.html')

@app.route('/image', methods=['POST'])
def upload_file():
	
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)

    return "Success"
  
#registeration page  
@app.route("/register",methods = ['POST'])
def register():
	'''
		args :  * password
				* name
				* email
				* phone
		inserts into table 'complainer'

		returns "Success"
	'''
	password = request.form['password']
	name = request.form['name']
	email = request.form['email']
	phone = request.form['phone']

	db = MySQLdb.connect("localhost","root","","hackathon")
	cursor = db.cursor()
	cursor.execute("INSERT INTO complainer (name,email,phone,password) VALUES('"+name+"','"+email+"','"+phone+"','"+password+"')")
	db.commit()
	db.close()
	return "Success"

@app.route("/login", methods = ['POST'])
def login():
	'''
		args:   *password
				*policeId
		Checks if any user exists in with that policeId and password

		returns Success or Failure accordingly
	'''
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

@app.route("/details",methods=['POST'])
def details():
	vehicle = request.form['vehicleNo']
	crime = request.form['crime']



	return




#license plate number and array and documents photo

## To run the Flask##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

