import MySQLdb
from flask import Flask, request, Response ,jsonify
import json
app = Flask(__name__)

# Open database connection
#db = MySQLdb.connect("localhost","root","","movie" )

# prepare a cursor object using cursor() method
#cursor = db.cursor()

# execute SQL query using execute() method.`

#cursor.execute("SELECT * FROM movie")

# Fetch a single row using fetchone() method.

#data = cursor.fetchone()
#print (data)

#print "Database version : %s " % data

@app.route('/login', methods = ['GET'])
def login():
	
	password = request.args.get('password')
	username = request.args.get('username')
	
	db = MySQLdb.connect("localhost","root","","movie")
	cursor = db.cursor()

	cursor.execute("SELECT * from user where username='" + username + "' and password='" + password + "'")
	pwd = cursor.fetchone()

	
	if (pwd):
		cursor.execute("SELECT city from user where username='" + username + "'")
		pwd = cursor.fetchone()

		db.close()
		return jsonify({"status":"Success","city":pwd[0]})
	else:
		db.close()
		return jsonify({"status":"Failed"})

@app.route('/register',methods=['GET'])
def register():
	username = request.args.get('username')
	password = request.args.get('password')
	email = request.args.get('email')
	mobile_no = request.args.get('mobile_no')
	city = request.args.get('city')
	db = MySQLdb.connect("localhost","root","","movie" )
	cursor = db.cursor()
	sql= "INSERT INTO user(username,password,email,mobile_no,balance,city) values('"+username+"','"+password+"','"+email+"','"+mobile_no+"',"+"0"+",'"+city+"')"
	
	try:
		cursor.execute(sql)
		db.commit()
		return jsonify({"status":"Success"})
	except:
		db.rollback()
		return jsonify({"status":"Failed"})
	db.close()

@app.route('/movies', methods=['GET'])
def movies():
	city = request.args.get('city')
	mov=[]

	db = MySQLdb.connect("localhost","root","","movie" )
	cursor = db.cursor()
	sql = "SELECT movie_id from screens where city='"+city+"' and date = (SELECT current_date())"
	cursor.execute(sql)
	result =cursor.fetchall()

	for r in result:
		movie_id=r[0]
		query = "SELECT * FROM movie WHERE movie_id = "+str(movie_id)
		cursor.execute(query)
		results =cursor.fetchall()
		for row in results:
			movie_name=row[1]
			movie_rating=row[2]
			release_date = row[3]
			description=row[4]
			img_url=row[5]
			empDict = {'movie_id':movie_id,'movie_name':movie_name,'movie_rating':movie_rating,'release_date':release_date,'description':description,'img_url':img_url}
			mov.append(empDict)
	jsonSt=jsonify(mov)
	db.close()
	return jsonSt
	
@app.route('/shows',methods=['GET'])
def shows():
	movie_id = request.args.get('movie_id')
	date = request.args.get('date')
	city = request.args.get('city')

	db = MySQLdb.connect("localhost","root","","movie" )
	cursor = db.cursor()

	show=[]
	sql = "SELECT screen_no, theatre_id, ticket_amt FROM screens WHERE movie_id="+movie_id+" and city ='"+city+"' and date ='"+date+"'"
	cursor.execute(sql)
	results =cursor.fetchall()
	for row in results:
		theatre_id = row[1]
		query = "SELECT theatre_name FROM theatre WHERE theatre_id= "+str(theatre_id)
		cursor.execute(query)
		theatre_name = cursor.fetchone()
		screen_no = row[0]	
		ticket_amt = row[2]

		query1= "SELECT time FROM screens WHERE movie_id="+movie_id+" and theatre_id= "+str(theatre_id)+" and screen_no ="+str(screen_no)
		cursor.execute(query1)
		timi = cursor.fetchall()
		time=[]
		for row in timi:
			time.append(row[0])
		
		
		empDict = {'theatre_id':theatre_id,'theatre_name':theatre_name[0],'screen_no':screen_no,'ticket_amt':ticket_amt,'time':time}
		show.append(empDict)
	jsonSt=jsonify(show)
	db.close()
	return jsonSt

@app.route('/seats', methods=['GET'])
def seat():
	movie_id=request.args.get('movie_id')
	theatre_id=request.args.get('theatre_id')
	screen_no=request.args.get('screen_no')
	time= request.args.get('time')
	date = request.args.get('date')

	db = MySQLdb.connect("localhost","root","","movie" )
	cursor = db.cursor()
	seats=[]
	sql= "SELECT seat_no from tickets WHERE movie_id= "+str(movie_id)+" and theatre_id ="+str(theatre_id)+" and screen_no= "+str(screen_no)+" and show_date ='"+date+"' and show_time= "+str(time)
	try:
		cursor.execute(sql)
		result =cursor.fetchall()
		for row in result:
			seats.append(row[0])
		return jsonify(seats)
		db.close()
		
	except:
		return jsonify({'status':'failed'})
		db.rollback()

@app.route('/book', methods=['GET'])
def book():
	movie_id=request.args.get('movie_id')
	theatre_id=request.args.get('theatre_id')
	screen_no=request.args.get('screen_no')
	time= request.args.get('time')
	date = request.args.get('date')
	username =request.args.get('username')
	ticket_amt = request.args.get('ticket_amt')
	seat_no= request.args.get('seat_no')

	db = MySQLdb.connect("localhost","root","","movie" )
	cursor = db.cursor()

	sql = "INSERT INTO tickets (ticket_amt,seat_no,show_date,show_time,username,movie_id,theatre_id,screen_no) VALUES ("+str(ticket_amt)+" ,"+str(seat_no)+" ,'"+date+"', "+str(time)+" ,'"+username+"' , "+str(movie_id)+" ,"+str(theatre_id)+" ,"+str(screen_no)+")"
	cursor.execute(sql)
	
	qw = "UPDATE user SET balance = balance - "+str(ticket_amt)+" WHERE username='"+username+"'"
	cursor.execute(qw)
	db.commit()
	db.close()
	return jsonify({"status":"Success"})

@app.route('/tickets', methods=['GET'])
def tickets():
	username =request.args.get('username')

	db = MySQLdb.connect("localhost","root","","movie" )
	cursor = db.cursor()

	sql = "SELECT * from tickets WHERE username='"+username+"'"
	cursor.execute(sql)
	results = cursor.fetchall()
	tickets=[]
	for row in results:
		empDict={'ticket_id':row[0],'ticket_amt':row[1],'seat_no':row[2],'show_date':row[3],'show_time':row[4],'movie_id':row[6],'theatre_id':row[7],'screen_no':row[8]}
		tickets.append(empDict)
	return jsonify(tickets)
# disconnect from server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)