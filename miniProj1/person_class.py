import sqlite3
import random, datetime

connection = None
cursor = None

# function for creating a person
#persons(fname, lname, bdate, bplace, address, phone) 
# creating a return with the info so that insertion of parameters are unnecessary
def createPerson():
	given = False
	while not given:
		fname = input("First name: ")
		lname = input("Last name: ")
		if fname is "" or lname is "":
			print("Missing primary key information (First Name, Last Name)")
		else:
			given = True
	bdate = input("Birth date (yyyy/mm/dd): ") # bdate is for person
	bplace = input("Birth place: ") # this is for person too
	address = input("Address: ")
	return fname, lname, bdate, bplace, address
	

# this function takes all the input in for a new birth
def getBirthInfo():
	fname = input("First name: ")
	lname = input("Last name: ")
	gender = input("Gender (M/F): ")
	f_fname = input ("Father's first name: ")
	f_lname = input("Father's last name: ")
	m_fname = input ("Mother's first name: ")
	m_lname = input("Mother's last name: ")
	# I am going to check here too ;)
	cursor.execute('''SELECT fname,lname from persons WHERE fname = ? AND lname = ?''',(fname, lname))
	pname = cursor.fetchall()
	if pname == []:
		person = createPerson()
		cursor.execute('''INSERT or REPLACE INTO persons VALUES (?,?,?,?,?)''',person)
		connection.commit()
	cursor.execute('''SELECT fname,lname from persons WHERE fname = ? AND lname = ?''',(f_fname, f_lname))
	p1name = cursor.fetchall()
	print(p1name)
	cursor.execute('''SELECT fname,lname from persons WHERE fname = ? AND lname = ?''',(m_fname, m_lname))
	p2name = cursor.fetchall()
	print(p2name)
	# checking done

	if pname == ("", ""):
		print("%s  %s does not exist", fname, lname)
	elif p1name == ("",""):
		print("You are giving father's information of a person who doesn't exist/nPlease provide the father's necessary information")
		father_info = createPerson()
		cursor.execute('''INSERT or REPLACE INTO persons VALUES (?,?,?,?,?)''', father_info)
		connection.commit()
	elif p2name == ("", ""):
		print("You are giving mother's information of a person who doesn't exist/nPlease provide the mother's necessary information")
		mother_info = createPerson()
		cursor.execute('''INSERT or REPLACE INTO persons VALUES (?,?,?,?,?)''', mother_info)
		connection.commit()
	else:
		regdate = getDate()
		regno = getUnique("births", "regno")
		regplace = 'Test' # this is going to be the user's registration place
		return regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname

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
	cursor.execute("SELECT %s from %s;" %(key,table))
	all = cursor.fetchall()
	
	#main functionality
	cursor.execute("SELECT %s FROM %s ORDER BY %s DESC limit 1;" %(key, table, key))
	num = cursor.fetchone()	
	for x in num:
		return x+1

#getting parents information like phone and address
def getParentInfo(fname, lname):
	global cursor, connection
	data = (fname, lname,)
	cursor.execute('''SELECT persons.address, persons.phone from persons, births
					WHERE births.m_fname = persons.fname AND births.m_lname = persons.lname
					AND births.fname = ? AND births.lname = ? ''' ,data)
	parent = cursor.fetchone()
	return parent

def getDate():
	now = datetime.datetime.now()
	date = now.strftime("%Y/%m/%d")
	return date

def main():
	global connection, cursor
	connect("./mp1.db")
	#sth = getUnique("births", "regno")
	#print(sth, x)

	#cursor.execute('''SELECT * from births''')
	#all = cursor.fetchall()
	#print(all)
	#parent = getParentInfo("Nasif2","Hossain2")
	cursor.execute('''INSERT or REPLACE INTO births VALUES (?,?,?,?,?,?,?,?,?,?)''', getBirthInfo())
	connection.commit()
	cursor.execute('''SELECT * from births''')
	all = cursor.fetchall()
	print("Congrats! test passed")

	print(all)
	
main()