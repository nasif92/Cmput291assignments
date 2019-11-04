import sqlite3
import random, datetime
import system



# function for creating a person
# persons(fname, lname, bdate, bplace, address, phone) 
# creating a return with the info so that insertion of parameters are unnecessary
# important!!! phone and address not given here for the first operation
def createPerson(fname, lname, child):
	global connection, cursor,database
	cursor = system.cursor
	connection = system.connection

	if fname == "" or lname == "":
		given = False
		while not given:
			fname = input("First name: ")
			lname = input("Last name: ")
			if fname is "" or lname is "":
				print("Missing primary key information (First Name, Last Name)")
			else:
				given = True
	else:
		print("Creating a person with the name: %s %s" %(fname,lname))
	bdate = input("Birth date (yyyy/mm/dd): ") # bdate is for person
	bplace = input("Birth place: ") # this is for person too
	address = ""
	phone = ""
	if not child:
		address = input("Enter address: ")
		phone = input ("Enter phone: ")
	return fname.capitalize(), lname.capitalize(), bdate, bplace, address, phone


# function for checking if a person is existent or not in the Person class
def getPerson(fname, lname):
	global connection, cursor, database
	cursor = system.cursor
	isPresent = False
	system.cursor.execute('''SELECT fname, lname from persons WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE''',(fname, lname,))
	personName = cursor.fetchall()
	for person in personName:
		if person[0].capitalize() == fname.capitalize() and person[1].capitalize() == lname.capitalize():
			isPresent = True
	return isPresent



# this one takes in table and executes and gives a unique key plus 1 the old one
def getUnique(table, key):
	global cursor, connection, database
	cursor = system.cursor

	# this is for checking if a key is already present
	# probably not required
	#main functionality
	cursor.execute("SELECT %s FROM %s ORDER BY %s DESC limit 1;" %(key, table, key))
	num = cursor.fetchone()	
	if num != None:
		for x in num:
			return int(x)+1
	else:
		return 1


def getDate():
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date

