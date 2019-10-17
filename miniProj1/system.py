

def main():
	# first screen
	print("Welcome to the program.")
	print("Enter your login details:")
	uid = input("User ID: ")
	pwd = input("Password: ")
	# compare these uid and pwd input variables with uid and pwd inside the users table.
	# be able to get the user type (Eg. registry agent) and put that into a variable

	operation_choice(user_type="registry agent")

	

	# The operations are different for each user type
	

	

	


def operation_choice(user_type):
	options_list = []
	print("Choose your operations: ")


	if user_type == "registry agent":
		print("blah blah")

		options_list = [
			"Register a birth", 
			"Register a marriage", 
			"Renew a vehicle registration", 
			"Process a bill of sale", 
			"Process a payment",
			"Get a driver abstract",
		]
	else if user_type == "traffic officer":
		print("poooooop")
		options_list = [
			"Issue a ticket",
			"Find a car owner"
		]

	for i in range(len(options)):
		print(options[i])


def register_a_birth():
	pass

main()