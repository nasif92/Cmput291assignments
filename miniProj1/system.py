import sqlite3

connection = None
cursor = None

def main():
	global connection, cursor
	connection = sqlite3.connect("./mp1.db")
	cursor = connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON;")
	connection.commit()

	# first screen
	print("Welcome to the program.")
	

	prompt = ''
	
	while prompt != 'q':
		print()
		print("Enter your login details:")
		uid = input("User ID: ")
		pwd = input("Password: ")
		print()
		# compare these uid and pwd input variables with uid and pwd inside the users table.
		# be able to get the user type (Eg. registry agent) and put that into a variable
		cursor.execute("select utype from users where uid=? and pwd=?", (uid, pwd))
		utype = cursor.fetchall()
		if not utype:
			print("The User Id and Password combination did not return any results.")
		else:
			# print(utype[0][0])
			operation_choice(utype[0][0])

		prompt = input("Press enter to continue, or q to exit this program: ")
		
	

	
	





def operation_choice(user_type):
	# The operations are different for each user type

	options_list = []
	print("Select an operation: ")
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
		choice = input("Enter the number corresponding to the desired operation: ")
		if choice == "1":
			issue_ticket()
		elif choice == "2":
			find_car_owner()


	

def issue_ticket():
	global cursor, connection
	regno = input("Please provide a registration number to view information: ")
	cursor.execute('''select fname, lname, make, model, year, color 
					  from registrations join vehicles using (vin)
					  where regno=?''', (regno,))
	rows = cursor.fetchall()
	if not rows:
		print("The provided registration number does not exist")
	else:
		info_for_regno = rows[0]
		print("Information for registration number:", regno)
		print()
		for column in info_for_regno:
			print(column, end="  ")
		print()
	

def find_car_owner():
	pass
def register_a_birth():
	pass

main()