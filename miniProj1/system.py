

def main():
	print("Welcome to the program.")
	print("Enter your login details:")
	username = input("User ID: ")
	password = input("Password: ")
	# Each user of the system should be able to login using a valid user id and password, 
	# denoted with uid and pwd in table users.
	print("Choose your operations:")

	# The operations are different for each user type
	registry_agent_options = [
		"Register a birth", 
		"Register a marriage", 
		"Renew a vehicle registration", 
		"Process a bill of sale", 
		"Process a payment",
		"Get a driver abstract",
		]

	traffic_officer_options = [
		"Issue a ticket",
		"Find a car owner"
		]

	for i in range(len(options)):
		print(options[i])



def register_a_birth():
	pass

main()