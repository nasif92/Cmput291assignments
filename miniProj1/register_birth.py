import sqlite3
import random, datetime
from person_class import createPerson, getPerson, getDate, getUnique


connection = None
cursor = None

def getBirthInfo(regplace):
	global connection, cursor
	given = False
	# check if child's information is given or not
	while not given:
		fname = input("First name: ")
		lname = input("Last name: ")
		if fname != "" and lname != "":
			given = True
		else:
			print("\nPlease input child's first name and last name.\n")
	gender = input("Gender (m/f): ")
	bdate = input("Birth date (yyyy-mm-dd): ") # bdate is for person
	bplace = input("Birth place: ") # this is for person too
	given = False
	while not given:	
		f_fname = input ("Father's first name: ")
		f_lname = input("Father's last name: ")
		if f_fname != "" and f_lname != "":
			given = True
		else:
			print("\nPlease input father's first name and last name\n")
	if (getPerson(f_fname, f_lname)): # if father is not a person, get the information about father
		print("\nFather's information is present in database\n")
	else:
		print("\nFather's information not in database. \nPlease provide the required information for creating a new person")
		father = createPerson(f_fname.capitalize(),f_lname.capitalize(),False)
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',father) # have to push parents to database
		print("Done! You created the father's information")
	given = False
	while not given: # check for first name and last name
		m_fname = input ("Mother's first name: ")
		m_lname = input("Mother's last name: ")
		if m_fname != "" and m_lname != "":
			given = True
		else:
			print("You have to input mother's both first name and last name")
	if (getPerson(m_fname, m_lname)): # if mother is not there get her information
		print("Mother's information is present in database")
		cursor.execute('''SELECT address,phone from persons WHERE fname = ? COLLATE NOCASE AND lname = ?
		COLLATE NOCASE''',(m_fname.capitalize(),m_lname.capitalize()))
		info = cursor.fetchall()
		address = info[0][0]  # mother's address
		phone = info[0][1] # mother's phone
		
	else:
		print("Mother is not there in your database. \nPlease provide the required information for creating a new person")
		mother = createPerson(m_fname.capitalize(), m_lname.capitalize(),False)
		address = mother[4]  # mother's address
		phone = mother[5] # mother's phone
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',mother) # have to push parents to database
		print("Done! You created the mother's information")
	#putting child into database
	cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',(fname, lname, bdate, bplace,address,phone)) 
	regdate = getDate()
	connection.commit()
	regno = getUnique("births", "regno") # getting a unique registration number
	#regplace = 'Test' # this is going to be the user's registration place

	return regno, fname, lname, regdate, regplace, gender, f_fname.capitalize(), f_lname.capitalize(), m_fname.capitalize(), m_lname.capitalize()


def register_a_birth(regplace):
	global cursor, connection

	connection = sqlite3.connect("./mp1.db")
	cursor = connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON;")
	connection.commit()

	prompt = input ("Register for birth? (y/n)")
	# have to find a unique registration number too
	if prompt == 'Y' or prompt == 'y':
		print("Putting into births database ...")
		# register that new person into registry
		cursor.execute('''INSERT or replace INTO births
		VALUES (?,?,?,?,?,?,?,?,?,?);''', getBirthInfo(regplace))
		# create a person				
		connection.commit()
		print("\nBirth successfully registered.\n")
	else:
		print("\nExiting prompt...\n")
