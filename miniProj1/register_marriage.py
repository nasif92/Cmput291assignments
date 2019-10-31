from person_class import createPerson, getPerson, getDate, getUnique
import sqlite3

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


import random, datetime
def register_marriage():
	global cursor, connection
	prompt = input ("Register marriage? (y/n) ")
	if prompt is 'y' or prompt is 'Y':
		given = False
		while not given:
			p1_fname = input("First Name of partner 1: ")
			p1_lname = input("Last Name of partner 1: ")
			if p1_fname != "" and p1_lname != "":
				given = True
			else:
				print("You have to provide partner 1's first name and last name")
		if (getPerson(p1_fname, p1_lname)): # if partner1 is not a person, get the information about partner
			print("Partner1's information is present in database")
		else:
			print("Person named %s %s is not there in your database. \nPlease provide the required information for creating a new person" %(p1_fname,p1_lname))
			partner1 = createPerson(p1_fname,p1_lname,False)
			cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',partner1) # have to push parents to database
			connection.commit()
			print("Done! You created the partner 1's (%s %s)'s information" %(p1_fname,p1_lname))
		given = False
		while not given:
			p2_fname = input("First Name of partner 2: ")
			p2_lname = input("Last Name of partner 2: ")
			if p2_fname != "" and p2_lname != "":
				given = True
			else:
				print("You have to provide partner 2's first name and last name")
		if (getPerson(p2_fname, p2_lname)): # if partner2 is not a person, get the information about partner
			print("Partner2's information is present in database")
		else:
			print("Person named %s %s is not there in your database. \nPlease provide the required information for creating a new person" %(p2_fname,p2_lname))
			partner2 = createPerson(p2_fname,p2_lname,False)
			cursor.execute('''INSERT or REPLACE INTO persons VALUES (?,?,?,?,?,?)''',partner2) # have to push parents to database
			connection.commit()
			print("Done! You created the partner 1's (%s %s)'s information" %(p2_fname,p2_lname))
		regno = getUnique("marriages","regno")
		regdate = getDate()
		regplace = "Test"
		cursor.execute('''INSERT or REPLACE INTO marriages VALUES(?,?,?,?,?,?,?)''',(regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname))
		connection.commit()
	else:
		print("Alright!")

def main():
	global connection, cursor
	connect("./test.db")
	# first screen	
main() 