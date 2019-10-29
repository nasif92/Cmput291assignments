import sqlite3
import random
import time
import datetime

connection = None
cursor = None

def main():
	global connection, cursor
	connection = sqlite3.connect("./mp1.db")
	cursor = connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON;")
	connection.commit()

	# first screen
	print("\nWelcome to the program.")
	
	utype = login_screen()

	while utype != 'q':
		logout = operation_choice(utype)
		if logout == True:
			utype = login_screen()

		# prompt = input("Press enter to continue, or q to close the program: ")
		
	

	
	


def login_screen():
	valid = False
	utype = ""
	while valid == False:
		print("\nEnter login details, or q to close the program:")
		uid = input("User ID: ")
		uid = uid.lower()
		pwd = input("Password: ")
		print()

		if uid == "q" or pwd == "q":
			utype = "q"
			break
		
		cursor.execute("select utype from users where uid=? and pwd=?", (uid, pwd))
		rows = cursor.fetchall()
		if not rows:
			print("The User Id and Password combination did not return any results.")
		else:
			valid = True
			utype = rows[0][0]

	return utype


def operation_choice(user_type):
	# The operations are different for each user type

	options_list = []
	
	print()

	if user_type == "a":
		print("Operations for Registry Agents:")
		print()
		options_list = [
			"Register a birth", 
			"Register a marriage", 
			"Renew a vehicle registration", 
			"Process a bill of sale", 
			"Process a payment",
			"Get a driver abstract",
		]
		
		complete = False
		while not complete:
			for i in range(len(options_list)):
				print(str(i+1)+". "+ options_list[i])
			print()

			print("Enter the number corresponding to the desired operation, ")
			choice = input("Or enter l to logout: ")
			if choice == "1":
				complete = register_a_birth()
			elif choice == "2":
				pass
			elif choice == "3":
				pass
			elif choice == "4":
				pass
			elif choice == "5":
				pass
			elif choice == "6":
				complete = get_driver_abstract()
			elif choice == "l":
				print("\nYou have logged out.\n")
				break

	elif user_type == "o":
		print("Operations for Traffic Officers:")
		print()
		options_list = [
			"Issue a ticket",
			"Find a car owner"
		]
		
		complete = False
		while not complete:
			for i in range(len(options_list)):
				print(str(i+1)+". "+ options_list[i])
			print()

			print("Enter the number corresponding to the desired operation, ")
			choice = input("Or enter l to logout: ")
			if choice == "1":
				complete = issue_ticket()
			elif choice == "2":
				complete = find_car_owner()
			elif choice == "l":
				print("\nYou have logged out.\n")
				break

	return True

def get_driver_abstract():
	global cursor, connection
	fname = input("Enter a first name: ")
	lname = input("Enter a last name: ")
	# Driver Abstract: which includes the number of tickets, the number of demerit notices,
	# the total number of demerit points received both within the past two years and within the lifetime.

	
	cursor.execute("select regno from registrations where fname=? and lname=?", (fname, lname))
	rows = cursor.fetchall()
	if not rows:
		print("\nThe first and last name entered did not match any registration number.\n")
		return False

	print(rows)
	getCount = '''
				select count(t.tno)
				from registrations r join tickets t using(regno)
				where r.regno=t.regno and r.fname=? and r.lname=?
			   '''
	cursor.execute(getCount, [fname, lname])
	ticketCount = cursor.fetchall()[0][0]
	print(ticketCount)
	return True

	
def find_car_owner():
	global cursor, connection
	# user provides one or more of make, model, year, color, and plate.

	# If there are more than 4 matches, you will show only the make, model, year, color, and the plate of the matching cars and let the user select one
	
	## i.e. more GENERAL
	# make, model, year, color, plate
	
	# When there are less than 4 matches or when a car is selected from a list 
	# shown earlier, for each match, the make, model, year, color, and the plate of 
	# the matching car will be shown as well as the latest registration date, the expiry date, 
	# and the name of the person listed in the latest registration record.
	
	## i.e. more PRECISE
	# make, model, year, color, plate, regdate, expiry, fname, lname

	finalQuery = '''select make, model, year, color, plate, regdate, expiry, fname, lname
	   				from registrations r join vehicles v using(vin) 
	   				where ''' # make='Porsche' and model='Boxter' and year='2017' and color='pink' and plate='CASSIE';	<--- Ideally
	make = input("make: ")
	model = input("model: ")
	year = input("year: ")
	color = input("color: ")
	plate = input("plate: ")
	
	parameters = []
	if make != "":
		finalQuery += "make=? and "#, (Porsche)
		# " and "
		parameters.append(make)
	if model != "":
		finalQuery += "model=? and "
		# " and "
		parameters.append(model)
	if year != "":
		finalQuery += "year=? and "
		# " and "
		parameters.append(year)
	if color != "":
		finalQuery += "color=? and "
		# " and "
		parameters.append(color)
	if plate != "":
		finalQuery += "plate=? and "
		# ";"
		parameters.append(plate)

	finalQuery = finalQuery[:-5]
	finalQuery += ";"
	# print(finalQuery)

	cursor.execute(finalQuery, parameters)
	rows = cursor.fetchall()
	count = 0
	for match in rows:
		count += 1

	if count > 4:
		# print(make, model, year, color, plate)
		pass
	else:
		# print(make, model, year, color, plate, regdate, expiry, fname, lname)
		pass


	return True

def issue_ticket():
	global cursor, connection
	
	regno = int(input("Please provide a registration number to view information: "))
	cursor.execute('''select fname, lname, make, model, year, color 
					  from registrations join vehicles using (vin)
					  where regno=?''', [regno])
	rows = cursor.fetchall()
	if not rows:
		print("The provided registration number does not exist")
		return False

	info_for_regno = rows[0]
	success = False
	while success == False:
		print("\nInformation for registration number:", regno)
		print()
		for column in info_for_regno:
			print(column, end="  ")
		print("\n")
		print("Issue a ticket to registration number: "+ str(regno) + "?")
		prompt = input("(Press Enter to ticket, q to exit): ")
		if prompt == "q":
			break

		print("Please provide the following information:\n")
		vdate = input("Violation date: ")

		if vdate == "":
			vdate = time.strftime("%Y-%m-%d")
		
		violation = input("Violation (text): ")

		fine = input("Fine amount: ")
		print()
		
		# generate a random tno, which might not be unique. An exception is used to handle this.
		tno = random.sample(range(100000, 999999), 1)[0]

		try:
			cursor.execute('''insert into tickets values
							   (?, ?, ?, ?, ?);''', (tno, regno, fine, violation, vdate))
			connection.commit()
			print("A ticket (tno: "+str(tno)+ ") has been issued to registration number " + str(regno) + ".")
			success = True
		except sqlite3.IntegrityError as nonUniqueTNO:
			print("An error occured while generating a TNO. Please try again.")

	return True
	





def register_a_birth():
	return True

main()