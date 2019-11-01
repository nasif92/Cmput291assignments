import getpass


def loginActivity():
	try:
		p = getpass.getpass(prompt='Password: ') 
		if p == "qwerty":
			print("That's cool!")
	except:
		print("Error happened")

def main():
	loginActivity()
main()