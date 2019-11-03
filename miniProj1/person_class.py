import sqlite3
import random, datetime

connection = None
cursor = None

# function for creating a person
# persons(fname, lname, bdate, bplace, address, phone) 
# creating a return with the info so that insertion of parameters are unnecessary
# important!!! phone and address not given here for the first operation
def createPerson(fname, lname, child):
	global connection, cursor
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
	return fname, lname, bdate, bplace, address, phone


# function for checking if a person is existent or not in the Person class
def getPerson(fname, lname):
	global connection, cursor
	isPresent = False
	cursor.execute('''SELECT fname, lname from persons WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE''',(fname, lname,))
	personName = cursor.fetchall()
	for person in personName:
		if person[0].capitalize() == fname.capitalize() and person[1].capitalize() == lname.capitalize():
			isPresent = True
	return isPresent

# not functional here
# this function takes all the input in for a new birth

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

# this one takes in table and executes and gives a unique key plus 1 the old one
def getUnique(table, key):
	global cursor, connection
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
#getting parents information like phone and address
# don't think it's necessary anymore
def getParentInfo(fname, lname):
	global cursor, connection
	data = (fname, lname,)
	cursor.execute('''SELECT persons.address, persons.phone from persons, births
					WHERE births.m_fname = persons.fname AND births.m_lname = persons.lname
					AND births.fname = ? COLLATE NOCASE AND births.lname = ? COLLATE NOCASE''' ,data)
	parent = cursor.fetchone()
	return parent

def getDate():
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date

def main():
	global connection, cursor
	connect("./mp1.db")
main()