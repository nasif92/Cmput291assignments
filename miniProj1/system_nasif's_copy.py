import sqlite3
import random, datetime
from test import getUnique, getDate, getParentInfo
from person_class import createPerson, getPerson
connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return
def logIn_prompt():
	pass

def getBirthInfo():
	global connection, cursor
	fname = input("First name: ")
	lname = input("Last name: ")
	gender = input("Gender (M/F): ")
	bdate = input("Birth date (yyyy/mm/dd): ") # bdate is for person
	bplace = input("Birth place: ") # this is for person too	
	f_fname = input ("Father's first name: ")
	f_lname = input("Father's last name: ")
	if (getPerson(f_fname, f_lname)): # if father is not a person, get the information about father
		print("Father's information is present in database")
	else:
		print("Father named %s %s is not there in your database. \nPlease provide the required information for creating a new person" %(f_fname,f_lname))
		father = createPerson(f_fname,f_lname,False)
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',father) # have to push parents to database
		print("Done! You created the father's (%s %s)'s information" %(f_fname,f_lname))
	m_fname = input ("Mother's first name: ")
	m_lname = input("Mother's last name: ")
	if (getPerson(m_fname, m_lname)): # if mother is not there get her information
		print("Mother information is present in database")
	else:
		print("Mother named %s %s is not there in your database. \nPlease provide the required information for creating a new person" %(m_fname,m_lname))
		mother = createPerson(m_fname, m_lname,False)
		address = mother[4]  # mother's address
		phone = mother[5] # mother's phone
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',mother) # have to push parents to database
		print("Done! You created the mother's (%s %s)'s information" %(m_fname,m_lname))
		#putting child into database
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',(fname, lname, bdate, bplace,address,phone)) 
	regdate = getDate()
	connection.commit()
	regno = getUnique("births", "regno") # getting a unique registration number
	regplace = 'Test' # this is going to be the user's registration place

	return regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname

#births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
#persons(fname, lname, bdate, bplace, address, phone) 
#regno is unique
#regplace is city of user
#regdate is today's date

def register_a_birth():
	global cursor, connection

	prompt = input ("Register for birth? (y/n)")
	# have to find a unique registration number too
	if prompt == 'Y' or 'y':
		try:
			print("Putting into births database ...")
			# register that new person into registry
			cursor.execute('''INSERT or replace INTO births
			VALUES (?,?,?,?,?,?,?,?,?,?);''',getBirthInfo())
			# create a person				
			connection.commit()
			print("Well done! You have registered a new birth")
		except:
			print("Keys missing")

def main():
	global connection, cursor
	connect("./test.db")
	# first screen
	print("Welcome to the program.")
	register_a_birth()
	cursor.execute('''SELECT fname, lname from births''')
	all = cursor.fetchall()
	print(all)
	connection.commit()
main()