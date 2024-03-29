import sqlite3
import datetime
import random
import system

def bill_of_sale():
	global connection, cursor,database
	cursor = system.cursor
	connection = system.connection

	print()
	vin_chosen = input("Please provide the vin of a car: ")

	# EXPERIMENTAL
	cursor.execute('''select vin, fname, lname, regdate
					  from registrations join vehicles using (vin)
					  WHERE vin = ? AND regdate = (
					  	SELECT MAX(regdate)
					  	FROM registrations join vehicles using (vin)
					  	WHERE vin = ?)''', [vin_chosen, vin_chosen]) 
	match = cursor.fetchall()

	# SELECT vin, fname, lname

	if not match:
		print("The vin number provided is INCORRECT")
		return False

	vin = match[0][0]
	fname = match[0][1]
	lname = match[0][2]

	selected_fname = input("Provide the first name of the current owner: ")

	if selected_fname.capitalize() != fname:
		print("You entered the incorrect first name of the owner, exiting function.")
		return False

	selected_lname = input("Provide the last name of the current owner: ")

	if selected_lname.capitalize() != lname:
		print("You entered the incorrect last name of the owner, exiting function.")
		return False

	select_owner_fname = input("Provide the first name of the new owner: ")

	select_owner_lname = input("Provide the last name of the new owner: ")


	cursor.execute('''select fname, lname
					  from persons
					  where fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE''', [select_owner_fname, select_owner_lname])

	result = cursor.fetchone()

	if not result:
		print("You did not print a name in the persons records")
		return False

	plate = input("Print out a valid license plate, maximum characters is 7 characters: ")

	if len(plate) > 7:
		print("You entered a plate with too many characters")
		return False

	owner_regdate = datetime.date.today() # "%d/%m/%Y"
	# print(owner_regdate)
	owner_expiry = datetime.date.today() + datetime.timedelta(days=1*365 + 1)

	cursor.execute('''UPDATE registrations
					  SET expiry =?
					  WHERE vin = ?''', [owner_regdate, vin])

	loop = 1;
	while loop:
		regno = random.sample(range(100000000, 999999999), 1)[0]
		try:	
			cursor.execute("INSERT INTO registrations values(?,?,?,?,?,?,?)", (regno, owner_regdate, owner_expiry, plate, vin, select_owner_fname.capitalize(), select_owner_lname.capitalize()))
			connection.commit()
			print("\nsuccess!\n")
			loop = 0
		except sqlite3.IntegrityError as nonUniqueTNO:
			print("\nAn error has occured generating a regno, try again\n")
	
	return True













