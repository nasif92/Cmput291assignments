import sqlite3
import random
import time
import datetime
import sys
import getpass

database = ""
city = ""

def main():
		global connection, cursor, database
		database = sys.argv[1]
		connection = sqlite3.connect("./" + database)
		cursor = connection.cursor()
		cursor.execute("PRAGMA foreign_keys=ON;")
		connection.commit()

		##### MUST INCLUDE PROMPT TO ENTER DATABASE PATH!!!! #####

		# first screen
		print("\nWelcome to the program.")
		
		utype = login_screen()

		while utype != 'q':
			logout = operation_choice(utype)
			if logout == True:
				utype = login_screen()

	

def login_screen():
	##### must counter SQL injection attacks and make the password non-visible at the time of typing! #####
	global city, connection, cursor, database

	valid = False
	utype = ""
	while valid == False:
		print("\nEnter login details, or q to close the program:")
		uid = input("User ID: ")
		if uid == "q":
			utype = "q"
			print("\nHave a nice day! \n")
			break
		uid = uid.lower()
		pwd = getpass.getpass(prompt="Password: ")
		print()

		
		
		cursor.execute("select utype, city, fname, lname from users where uid=? COLLATE NOCASE and pwd=?", (uid, pwd))
		rows = cursor.fetchall()
		if not rows:
			print("The User Id and Password combination did not return any results.")
		else:
			valid = True
			utype = rows[0][0]
			city = rows[0][1]
			fname = rows[0][2]
			lname = rows[0][3]
			print("\nWelcome to the program %s %s" %(fname,lname))

	return utype


def operation_choice(user_type):
	# The operations are different for each user type
	global connection, cursor, database
	options_list = []
	
	print()

	if user_type == "a":
		
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
			print("Operations for Registry Agents:")
			print()
			for i in range(len(options_list)):
				print(str(i+1)+". "+ options_list[i])
			print()

			print("Enter the number corresponding to the desired operation, ")
			choice = input("Or enter l to logout: ")
			if choice == "1":
				register_a_birth(city)
			elif choice == "2":
				register_marriage(city)
			elif choice == "3":
				renew_registration()
			elif choice == "4":
				bill_of_sale()
			elif choice == "5":
				process_payment()
			elif choice == "6":
				get_driver_abstract()
			elif choice == "l":
				print("\nYou have logged out.\n")
				complete = True

	elif user_type == "o":
		
		options_list = [
			"Issue a ticket",
			"Find a car owner"
		]
		
		complete = False
		while not complete:
			print("Operations for Traffic Officers:")
			print()
			for i in range(len(options_list)):
				print(str(i+1)+". "+ options_list[i])
			print()

			print("Enter the number corresponding to the desired operation, ")
			choice = input("Or enter l to logout: ")
			if choice == "1":
				issue_ticket()
			elif choice == "2":
				find_car_owner()
			elif choice == "l":
				print("\nYou have logged out.\n")
				complete = True
				# break

	return True

# register birth
def getBirthInfo(regplace):
	
	global connection, cursor, database
	
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
	
	global cursor, connection

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

#register marriage
def register_marriage(regplace):
	global connection, cursor,database
	

	prompt = input ("Register marriage? (y/n) ")
	print()
	if prompt is 'y' or prompt is 'Y':
		given = False
		while not given:
			p1_fname = input("First Name of partner 1: ")
			p1_lname = input("Last Name of partner 1: ")
			if p1_fname != "" and p1_lname != "":
				given = True
			else:
				print("\nYou must provide partner 1's first name and last name")
		
		if (getPerson(p1_fname, p1_lname)): # if partner1 is not a person, get the information about partner
			print("\nPartner1's information is present in database\n")
		else:
			print("\nPerson named %s %s is not in the database. \nPlease provide the required information for creating a new person" %(p1_fname,p1_lname))
			print()
			choice = input("Record new information for partner 1? (y/n): ")
			choice = choice.lower()
			if choice != "y":
				print("\nExiting\n")
				return False
			
			partner1 = createPerson(p1_fname,p1_lname, False)
			cursor.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?)''', partner1) # have to push parents to database
			connection.commit()
			print("\nDone! You created the partner 1's (%s %s)'s information" %(p1_fname,p1_lname))

		given = False
		while not given:
			p2_fname = input("First Name of partner 2: ")
			p2_lname = input("Last Name of partner 2: ")
			if p2_fname != "" and p2_lname != "":
				given = True
			else:
				print("\nYou must provide partner 2's first name and last name")

		if (getPerson(p2_fname, p2_lname)): # if partner2 is not a person, get the information about partner
			print("\nPartner2's information is present in database\n")
		else:
			print("\nPerson named %s %s is not in the database. \nPlease provide the required information for creating a new person" %(p2_fname,p2_lname))
			print()
			choice = input("Record new information for partner 2? (y/n): ")
			choice = choice.lower()
			if choice != "y":
				print("\nExiting\n")
				return False

			partner2 = createPerson(p2_fname,p2_lname,False)
			cursor.execute('''INSERT or REPLACE INTO persons VALUES (?,?,?,?,?,?)''',partner2) # have to push parents to database
			connection.commit()
			print("\nDone! You created the partner 1's (%s %s)'s information" %(p2_fname,p2_lname))

		regno = getUnique("marriages","regno")
		regdate = getDate()

		# needed to capitalize to get rid of foreign constraint
		cursor.execute('''INSERT or REPLACE INTO marriages VALUES(?,?,?,?,?,?,?)''',(regno, regdate, regplace, p1_fname.capitalize(), p1_lname.capitalize(), p2_fname.capitalize(), p2_lname.capitalize()))
		connection.commit()
		print("\nMarriage of", p1_fname, p1_lname, "and", p2_fname, p2_lname, "successfully registed.\n")
		
	else:
		print("\nExiting prompt...\n")



# renew registration
def renew_registration():

	global connection, cursor,database
	
	try:
		regno = int(input("Enter a registration number to renew: "))
	
		rows = cursor.execute("select regno from registrations where regno=?", [regno])
		if not rows:
			print("That registration number does not exist.")
			return False

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
				cursor.execute('''UPDATE registrations set regdate=?, expiry = ? WHERE regno = ?''',(currentDate, newDate, regno))
				print("\nVehicle registration renewed!\n")
				connection.commit()
			except:
				print("Given registration number %s is not present in database\nExiting prompt...\n" %regno)
		else:
			print("\nExiting prompt...\n")
	except:
		print("\nInvalid registration number. It should be an integer\nExiting prompt...\n")



# bill of sale
def bill_of_sale():

	global connection, cursor,database
	
	print()
	vin_chosen = input("Please provide the vin of a car: ")

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
		return False

	vin = match[0][0]
	fname = match[0][1]
	lname = match[0][2]

	selected_fname = input("Provide the first name of the current owner: ")

	if selected_fname.capitalize() != fname:
		print("You entered the incorrect first name of the owner, exiting function.")
		return False

	selected_lname = input("Provide the last name of the current owner: ")

	if selected_lname.capitalize() != lname:
		print("You entered the incorrect last name of the owner, exiting function.")
		return False

	select_owner_fname = input("Provide the first name of the new owner: ")

	select_owner_lname = input("Provide the last name of the new owner: ")


	cursor.execute('''select fname, lname
					  from persons
					  where fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE''', [select_owner_fname, select_owner_lname])

	result = cursor.fetchone()

	if not result:
		print("You did not print a name in the persons records")
		return False

	plate = input("Print out a valid license plate, maximum characters is 7 characters: ")

	if len(plate) > 7:
		print("You entered a plate with too many characters")
		return False

	owner_regdate = datetime.date.today() # "%d/%m/%Y"
	# print(owner_regdate)
	owner_expiry = datetime.date.today() + datetime.timedelta(days=1*365 + 1)

	cursor.execute('''UPDATE registrations
					  SET expiry =?
					  WHERE vin = ?''', [owner_regdate, vin])

	loop = 1;
	while loop:
		regno = random.sample(range(100000000, 999999999), 1)[0]
		try:	
			cursor.execute("INSERT INTO registrations values(?,?,?,?,?,?,?)", (regno, owner_regdate, owner_expiry, plate, vin, select_owner_fname.capitalize(), select_owner_lname.capitalize()))
			connection.commit()
			print("\nsuccess!\n")
			loop = 0
		except sqlite3.IntegrityError as nonUniqueTNO:
			print("\nAn error has occured generating a regno, try again\n")
	
	return True


# find car owner
def find_car_owner():

	global connection, cursor,database


	# user provides one or more of make, model, year, color, and plate.
	
	# will concatenate at least one condition according to provided input
	
	print()
	success = False
	while success == False:
		finalQuery = '''select make, model, year, color, plate, regdate, expiry, fname, lname
						from registrations r join vehicles v using(vin) 
						where '''
		make = input("make: ")
		model = input("model: ")
		year = input("year: ")
		color = input("color: ")
		plate = input("plate: ")

		parameters = []
		if make != "":
			finalQuery += "make=? COLLATE NOCASE and "
			parameters.append(make)
			success = True
		if model != "":
			finalQuery += "model=? COLLATE NOCASE and "
			parameters.append(model)
			success = True
		if year != "":
			finalQuery += "year=? and "
			parameters.append(year)
			success = True
		if color != "":
			finalQuery += "color=? COLLATE NOCASE and "
			parameters.append(color)
			success = True
		if plate != "":
			finalQuery += "plate=? COLLATE NOCASE and "
			parameters.append(plate)
			success = True

		if success == False:
			print("\nPlease provide at least one of the fields.")
			prompt = input("(Press Enter to try again, q to exit): ")
			print()
			if prompt == "q":
				return False
		else:
			finalQuery = finalQuery[:-5]
			# finalQuery += " COLLATE NOCASE"
			print(finalQuery)
			cursor.execute(finalQuery, parameters)
			rows = cursor.fetchall()
			count = 0
			for match in rows:
				count += 1

			if count == 0:
				success = False
				print("\nYour query returned", count, "matches.")
				refine = input("(Press Enter to search again, q to exit): ")
				print()
				if refine == "q":
					return False

			elif count >= 4: # show only the make, model, year, color, and the plate of the matching cars and let the user select one
				print("\n4 or more matches.\n")
				num = 1
				for match in rows:
					print(str(num)+".", end=" ")
					for i in range(len(match)):
						if i in [0, 1, 2, 3, 4]:	
							print(match[i], end=" ")
					print()
					num += 1
				print()
				choiceNum = int(input("Enter the number corresponding to a match for more details: "))
				print()
				for column in rows[choiceNum-1]: # show the make, model, year, color, plate, regdate, expiry, fname, lname
					print(column, end=" ")
				print("\n")

			elif count < 4: # show the make, model, year, color, plate, regdate, expiry, fname, lname
				print("\nLess than 4 matches.\n")
				num = 1
				for match in rows:
					print(str(num)+".", end=" ")
					for column in match:
						print(column, end=" ")
					print()
					num += 1
				print()


	return True





def process_payment():
	global connection, cursor,database



	# tickets(tno, regno, fine, violation, vdate)
	# payments(tno, pdate, amount)
	print()
	tno = input("Enter a valid ticket number: ")

	cursor.execute('''SELECT tno, fine
					  FROM tickets
					  WHERE tno=?''', [tno])
	match = cursor.fetchone()

	if not match:
		print("The ticket number provided is INCORRECT")
		return False

	tno = match[0]
	fine = match[1]

	cursor.execute('''SELECT amount
					  FROM payments
					  WHERE tno = ?''', [tno])

	all_fines = cursor.fetchall()

	total_payment = 0;
	# print(all_fines)
	if all_fines:
		for amount in all_fines[0]:
			total_payment = total_payment + amount

	if total_payment == fine:
		print("\nThe fine has already been payed in full.\n")
		return False


	# try:
	print("\nFine left to pay for is currently $"+ str(fine - total_payment))
	print()
	payment = int(input("Enter a payment amount: "))
	# except:
	# 	print("You failed to enter a proper amount of payment")
	# 	return False

	if payment < 0:
		print("You entered an amount less than zero")
		return False

	if payment > fine - total_payment:
		print("You entered an amount higher than the fine")
		return False

	pdate = datetime.date.today()
	updated = total_payment + payment
	# print(updated)
	try:
		cursor.execute('''INSERT INTO payments VALUES(?,?,?)''', [tno, pdate, payment])
	except sqlite3.IntegrityError:
		cursor.execute('''update payments set amount=?, pdate=? where tno=?''', [updated, pdate, tno])

	connection.commit()

	new_fine = fine - total_payment - payment

	if new_fine == 0:
		print("\nYou have successfully payed off all of your fine.")
		print()
		return True

	else:
		print("\nTransaction processed, you still need to pay: $" + str(new_fine))
		print()
		return True






def get_driver_abstract():	

	global connection, cursor,database

	given =False
	quit = False

	while not given:
		prompt = ""
		fname = input("Enter fname: ")
		lname = input("Enter lname: ")
		if fname == "" or lname == "":
			print("Please input both first name and last name")
		if getPerson(fname,lname):
			given = True
		else:
			prompt = input ("Person named %s %s is not in database. Press q to quit: " %(fname, lname))
			if prompt == "q":
				quit = True
				print()
			given = True

	if given and not quit:
		cursor.execute('''SELECT count(DISTINCT tno) as got_tickets , COUNT(distinct demeritNotices.ddate) AS NOTICES
							from demeritNotices left outer join registrations using (fname,lname)
							left outer join tickets using (regno)
							WHERE date(demeritNotices.ddate) >= date('now','-2 years') 
							AND fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP BY fname, lname''',(fname,lname))
		data_2years = cursor.fetchone()
		cursor.execute('''SELECT count(DISTINCT tno) as got_tickets , COUNT(distinct demeritNotices.ddate) AS NOTICES
							from demeritNotices left outer join registrations using (fname,lname)
							left outer join tickets using (regno)
							WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP BY fname, lname''',(fname,lname))
		data_lifetime = cursor.fetchone()
		cursor.execute('''SELECT sum(demeritNotices.points) FROM demeritNotices
							WHERE date(ddate) >= date('now','-2 years')
							AND fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP by fname, lname''',(fname,lname,))
		points_2years = cursor.fetchone()
		cursor.execute('''SELECT sum(demeritNotices.points) FROM demeritNotices
							WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP by fname, lname''',(fname,lname,))
		points_lifetime = cursor.fetchone()
		cursor.execute('''SELECT tno, vdate,violation,fine,regno, make, model
							from (SELECT * from tickets
								left outer join registrations using (regno)
								left outer JOIN vehicles USING (vin)
								ORDER by vdate DESC
								)
								WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE''',(fname,lname,))
		tickets = cursor.fetchall()
		print(30*"=")

		print("Name: %s %s" %(fname.capitalize(),lname.capitalize()))
		print(30*"=")

		print("Over the last two years: ")
		print("Number of tickets: %s \nNumber of demerit notices: %s\nTotal number of demerit points: %s" %(data_2years[0],data_2years[1],points_2years[0]))
		print(30*"=")
		print("Over the lifetime of %s %s: " %(fname.capitalize(),lname.capitalize()))
		print("Number of tickets: %s \nNumber of demerit notices: %s\nTotal number of demerit points: %s" %(data_lifetime[0],data_lifetime[1],points_lifetime[0]))
		print(30*"=")
		print("All 5 latest tickets from in sorted order from latest to oldest: ")
		print(30*"=")
		i = 0
		if len(tickets) == 0:
			print("None")
		else:
			while i < 5 and i < len(tickets):
				print("ticket number: %s, violation date: %s \nviolation description: %s, fine: %s, registration number: %s \nmake: %s, model of car: %s" %(tickets[i][0],tickets[i][1],tickets[i][2],tickets[i][3],tickets[i][4],tickets[i][5],tickets[i][6])) 
				print(30*"=")
				i += 1
			if  len(tickets) > 5:
				prompt = input("Would you like to see more?: (y/n)")
				if prompt is "y" or prompt is "Y":
					while i < len(tickets):
						print("ticket number: %s, violation date: %s \nviolation description: %s, fine: %s, registration number: %s \nmake: %s, model of car: %s" %(tickets[i][0],tickets[i][1],tickets[i][2],tickets[i][3],tickets[i][4],tickets[i][5],tickets[i][6])) 
						print(30*"=")
						i+= 1
	print("\nExiting!\n")






def issue_ticket():
	global connection, cursor, database
	

	try: 
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
				return False

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
	except:
		print("\nYou put an invalid registration number. \nExiting\n")

	return True




def createPerson(fname, lname, child):

	global connection, cursor,database


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
	isPresent = False
	cursor.execute('''SELECT fname, lname from persons WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE''',(fname, lname,))
	personName = cursor.fetchall()
	for person in personName:
		if person[0].capitalize() == fname.capitalize() and person[1].capitalize() == lname.capitalize():
			isPresent = True
	return isPresent



# this one takes in table and executes and gives a unique key plus 1 the old one
def getUnique(table, key):

	global cursor, connection, database

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


main()