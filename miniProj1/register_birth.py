import sqlite3
import random, datetime
from person_class import createPerson, getPerson, getDate, getUnique


connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def getBirthInfo():
	global connection, cursor
	given = False
	# check if child's information is given or not
	while not given:
		fname = input("First name: ")
		lname = input("Last name: ")
		if fname != "" and lname != "":
			given = True
		else:
			print("You have to input child's both first name and last name")
	gender = input("Gender (M/F): ")
	bdate = input("Birth date (yyyy/mm/dd): ") # bdate is for person
	bplace = input("Birth place: ") # this is for person too
	given = False
	while not given:	
		f_fname = input ("Father's first name: ")
		f_lname = input("Father's last name: ")
		if f_fname != "" and f_lname != "":
			given = True
		else:
			print("You have to input father's both first name and last name")
	if (getPerson(f_fname, f_lname)): # if father is not a person, get the information about father
		print("Father's information is present in database")
	else:
		print("Father's information not in database. \nPlease provide the required information for creating a new person")
		father = createPerson(f_fname,f_lname,False)
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
		cursor.execute('''SELECT address,phone from persons WHERE fname = ? AND lname = ?''',(m_fname,m_lname))
		info = cursor.fetchall()
		address = info[0][0]  # mother's address
		phone = info[0][1] # mother's phone
		
	else:
		print("Mother is not there in your database. \nPlease provide the required information for creating a new person")
		mother = createPerson(m_fname, m_lname,False)
		address = mother[4]  # mother's address
		phone = mother[5] # mother's phone
		cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''',mother) # have to push parents to database
		print("Done! You created the mother's information")
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
	if prompt == 'Y' or prompt == 'y':
		try:
			print("Putting into births database ...")
			# register that new person into registry
			cursor.execute('''INSERT or replace INTO births
			VALUES (?,?,?,?,?,?,?,?,?,?);''',getBirthInfo())
			# create a person				
			connection.commit()
			print("Well done! You have registered a new birth")
		except:
			print("There is an error in the implementation. Sorry :(")
	else:
		print("Alright!")

# register a marriage
# marriages(regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)

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


# registrations(regno, regdate, expiry, plate, vin, fname, lname)
def renew_registration(regno):
	global cursor, connection
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
			cursor.execute('''UPDATE registrations set expiry = ? WHERE regno = ?''',(newDate,regno))
			connection.commit()
		except:
			print("Given registration number %s is not present in database" %regno)
	else:
		print("Alright!")
def main():
	global connection, cursor
	connect("./test.db")
	# first screen
	print("Welcome to the program.")
	register_a_birth() # this is functional already
	register_marriage()
	renew_registration(999999999) # this is functional too

	connection.commit()
	print("Every birth : ")
	print(40*"=")
	cursor.execute('''SELECT * from births''')
	all = cursor.fetchall()
	#print(all)
	print("Every marriage : ")
	print(40*"=")
	cursor.execute('''SELECT * from marriages''')
	all = cursor.fetchall()
	print(all)
	print("Every registrations : ")
	print(40*"=")
	cursor.execute('''SELECT * from registrations''')
	all = cursor.fetchall()
	#print(all)
	print("Every person : ")
	print(40*"=")
	cursor.execute('''SELECT * from persons''')
	all = cursor.fetchall()
	#print(all)

	#renew_registration(999999999)
	#print(regno)
main() 