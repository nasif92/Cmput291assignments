import sqlite3

def main():
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

		options_list = [
			"Register a birth", 
			"Register a marriage", 
			"Renew a vehicle registration", 
			"Process a bill of sale", 
			"Process a payment",
			"Get a driver abstract",
		]
	elif user_type == "o":
		print("Operations for Traffic Officers:")
		options_list = [
			"Issue a ticket",
			"Find a car owner"
		]

	for i in range(len(options_list)):
		print(options_list[i])


def register_a_birth():
	pass

main()