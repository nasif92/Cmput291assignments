import sqlite3
import random

connection = None
cursor = None
uniqueTNOs = []

def main():
	global connection, cursor
	connection = sqlite3.connect("./mp1.db")
	cursor = connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON;")
	connection.commit()

	# first screen
	print("Welcome to the program.")
	
	valid = False
	while valid == False:
		print("\nEnter your login details:")
		uid = input("User ID: ")
		pwd = input("Password: ")
		print()
		cursor.execute("select utype from users where uid=? and pwd=?", (uid, pwd))
		utype = cursor.fetchall()
		if not utype:
			print("The User Id and Password combination did not return any results.")
		else:
			valid = True

	prompt = ''
	while prompt != 'q':
		operation_choice(utype[0][0])

		prompt = input("Press enter to continue, or q to close the program: ")
		
	

	
	





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
		for i in range(len(options_list)):
			print(str(i+1)+". "+ options_list[i])
		print()
	elif user_type == "o":
		print("Operations for Traffic Officers:")
		options_list = [
			"Issue a ticket",
			"Find a car owner"
		]
		for i in range(len(options_list)):
			print(str(i+1)+". "+ options_list[i])
		print()
		complete = False
		while not complete:
			print("Enter the number corresponding to the desired operation, ")
			choice = input("Or enter q to exit this prompt: ")
			if choice == "1":
				complete = issue_ticket()
			elif choice == "2":
				complete = find_car_owner()
			elif choice == "q":
				break


	

def issue_ticket():
	global cursor, connection, uniqueTNOs
	# Make sure to change input value for regno to int!!
	regno = input("\nPlease provide a registration number to view information: ")
	cursor.execute('''select fname, lname, make, model, year, color 
					  from registrations join vehicles using (vin)
					  where regno=?''', (regno,))
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
		prompt = input("(Press Enter to continue, q to exit): ")
		if prompt == "q":
			break

		print("Please provide the following information:\n")
		vdate = input("Violation date: ")

		# The violation date should be set to today's date if it is not provided.
		violation = input("Violation (text): ")
		
		fine = input("Fine amount: ")
		print()
		
		# generate a random tno, which might not be unique. An exception is used to handle this.
		tno = random.sample(range(100000, 999999), 1)[0]

		try:
			cursor.execute('''insert into tickets values
							   (?, ?, ?, ?, ?);''', (tno, regno, fine, violation, vdate))
			connection.commit()
			print("A ticket (tno: "+str(tno)+ ") has been issued to registration number " + regno + ".")
			success = True
		except sqlite3.IntegrityError as nonUniqueTNO:
			print("An error occured while generating a TNO. Please try again.")

	
	

	
	

	return True
	

def find_car_owner():
	return True
def register_a_birth():
	pass

main()