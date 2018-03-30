import threading, zipfile
import time
import MySQLdb

class AsyncZip(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while(True):
			time.sleep(24*3600)
			self.check_reminders()
	def check_reminders():
		db=MySQLdb.connect("localhost","root","","hackathon")
		cursor = db.cursor()
		cursor.execute("SELECT rNo,caseNo from vehicaldetails where reminder=1")
		rows=cursor.fetchall()
		if(rows):
			for row in rows:
				lpno=row[0]
				cursor.execute("SELECT phone from vehicaldetails where rNo='{}'".format(lpno))
				mob=cursor.fetchone
				message.sms("Reminder",mob)
				cursor.execute("UPDATE cases set reminder=5 where caseNo="+str(row[1]))

background = AsyncZip()
background.start()
print('The main program continues to run in foreground.')

background.join()    # Wait for the background task to finish
print('Main program waited until background was done.')