import sqlite3
import random, datetime
from person_class import createPerson, getPerson, getDate, getUnique
import system
# registrations(regno, regdate, expiry, plate, vin, fname, lname)
def renew_registration():

	global connection, cursor,database
	cursor = system.cursor
	connection = system.connection

	try:
		regno = int(input("Enter a registration number to renew: "))
	
		rows = cursor.execute("select regno from registrations where regno=?", [regno])
		if not rows:
			print("That registration number does not exist.")
			return False

		prompt = input ("Renew registration for regno: %s? (y/n) " %regno)
		if prompt is 'y' or prompt is 'Y':
			try:
				cursor.execute('''SELECT expiry from registrations WHERE regno = ?''', (regno,))
				expiry = cursor.fetchone()
				currentDate = getDate()
				start = datetime.datetime.strptime(expiry[0],"%Y-%m-%d")
				end = datetime.datetime.strptime(currentDate,"%Y-%m-%d")
				diff = (start - end).days
				# today's date plus one year if negative
				# else plus one year that day given
				if diff <= 0:
					newDate = str(int(currentDate[0:4]) + 1) + datetime.datetime.now().strftime("-%m-%d")
				else:
					newDate = str(int(expiry[0][0:4]) + 1) + expiry[0][4:]
				cursor.execute('''UPDATE registrations set regdate=?, expiry = ? WHERE regno = ?''',(currentDate, newDate, regno))
				print("\nVehicle registration renewed!\n")
				connection.commit()
			except:
				print("Given registration number %s is not present in database\nExiting prompt...\n" %regno)
		else:
			print("\nExiting prompt...\n")
	except:
		print("\nInvalid registration number. It should be an integer\nExiting prompt...\n")