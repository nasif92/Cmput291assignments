import sqlite3
import random, datetime, system
from person_class import createPerson, getPerson, getDate, getUnique

# function for getting all the information about birth and returning all the information
# it also checks if a person is already in database or not, if not, it creates a new record of person
def getBirthInfo(regplace):
	global connection, cursor, database
	cursor = system.cursor
	connection = system.connection
	given = False
	# check if child's information is given or not
	while not given:
		fname = input("First name: ")
		lname = input("Last name: ")
		if getPerson(fname, lname):
			print("Sorry, the person named %s %s is already in the database" %(fname, lname))
			return False
		elif fname != "" and lname != "":
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
		print("\nDone! You created the father's information\n")
	given = False
	while not given: # check for first name and last name
		m_fname = input ("Mother's first name: ")
		m_lname = input("Mother's last name: ")
		if m_fname != "" and m_lname != "":
			given = True
		else:
			print("You have to input mother's both first name and last name")
	if (getPerson(m_fname, m_lname)): # if mother is not there get her information
		print("\nMother's information is present in database\n")
		cursor.execute('''SELECT address,phone from persons WHERE fname = ? COLLATE NOCASE AND lname = ?
		COLLATE NOCASE''',(m_fname.capitalize(),m_lname.capitalize()))
		info = cursor.fetchall()
		address = info[0][0]  # mother's address
		phone = info[0][1] # mother's phone
		
	else:
		print("\nMother is not there in your database. \nPlease provide the required information for creating a new person\n")
		mother = createPerson(m_fname.capitalize(), m_lname.capitalize(),False)
		address = mother[4]  # mother's address
		phone = mother[5] # mother's phone
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',mother) # have to push parents to database
		print("\nDone! You created the mother's information\n")
	#putting child into database
	cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',(fname.capitalize(), lname.capitalize(), bdate, bplace,address,phone)) 
	regdate = getDate()
	connection.commit()
	regno = getUnique("births", "regno") # getting a unique registration number

	return regno, fname.capitalize(), lname.capitalize(), regdate, regplace, gender, f_fname.capitalize(), f_lname.capitalize(), m_fname.capitalize(), m_lname.capitalize()


def register_a_birth(regplace):
	global cursor, connection, database
	cursor = system.cursor
	connection = system.connection

	prompt = input ("Register for birth? (y/n): ")
	# have to find a unique registration number too
	if prompt == 'Y' or prompt == 'y':
		print("\nPutting into births database ...\n")			
		# register that new person into registry
		birth_data = getBirthInfo(regplace)
		if birth_data != False:
			cursor.execute('''INSERT or replace INTO births
			VALUES (?,?,?,?,?,?,?,?,?,?);''', birth_data)
			# create a person				
			connection.commit()
			print("\nBirth successfully registered.\n")

		else:
			print("\nExiting prompt...\n")
	else:
		print("\nExiting prompt...\n")

