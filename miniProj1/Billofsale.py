import sqlite3
import datetime
import random

global cursor, connection

connection = sqlite3.connect("./mp1.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys=ON;")
connection.commit()

vin_chosen = input("Please provide the vin # of a car: ")


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
	# return False

vin = match[0][0]
fname = match[0][1]
lname = match[0][2]

selected_fname = input("Provide the first name of the owner: ")

if selected_fname != fname:
	print("You entered the incorrect first name of the owner, exiting function.")
	# return False

selected_lname = input("Provide the last name of the owner: ")

if selected_lname != lname:
	print("You entered the incorrect last name of the owner, exiting function.")
	# return False

select_owner_fname = input("Provide the first name of the new owner: ")

select_owner_lname = input("Provide the last name of the new owner: ")


cursor.execute('''select fname, lname
				  from persons
				  where fname=? AND lname=?''', [select_owner_fname, select_owner_lname])

result = cursor.fetchone()

if not result:
	print("You did not print a name in the persons records")
	# return False

plate = input("Print out a valid lisence plate, maximum characters is 7 characters: ")

if len(plate) > 7:
	print("You entered a plate with too many characters")
	# return False

owner_regdate = datetime.date.today() # "%d/%m/%Y"
# print(owner_regdate)
owner_expiry = datetime.date.today() + datetime.timedelta(days=1*365)

cursor.execute('''UPDATE registrations
				  SET expiry =?
				  WHERE vin = ?''', [owner_regdate, vin])

loop = 1;
while loop:
	regno = random.sample(range(100000000, 999999999), 1)[0]
	try:	
		cursor.execute("INSERT INTO registrations values(?,?,?,?,?,?,?)", (regno, owner_regdate, owner_expiry, plate, vin, select_owner_fname, select_owner_lname))
		connection.commit()
		print("success!")
		loop = 0
	except sqlite3.IntegrityError as nonUniqueTNO:
		print("An error has occured generating a regno, try again")
	
# return True













