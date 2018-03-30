import MySQLdb
from flask import Flask, request, Response ,jsonify, render_template
import numpy as np
import os

@app.route("/login")
def login():

	policeId = request.form['policeId']
	password = request.form['password']

	db = MySQLdb.connect("localhost","root","","hackathon")
	cursor = db.cursor()
	cursor.execute("select location from policedetails where policeId='{}' and password = '{}'".format(policeId, password
	row = cursor.fetchone()

	if(row):
		session['policeId'] = policeId
		session['location'] = location
		db.close()
		return render_template("dashboard.html")

	else:
		return "Failed"


@app.route("/dashboard")
def dashboard():


	
	db = MySQLdb.connect("localhost","root","","hackathon")

	cursor = db.cursor()
	cursor.execute("select * from complain where location= (select location from policedetails where policeId= '{}'".format(policeId)))
	rows = cursor.fetchall()

	if (rows):
		db.close()
		return render_template("complainList.html",rows = rows)   #Change the template name
		
	else:
		db.close()
		return "Failed"

'''
@app.route("/complainList")
def complainList():
	# Take policeId from session.
	rows = 

'''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
