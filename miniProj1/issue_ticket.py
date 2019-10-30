import sqlite3
import random
import time

def issue_ticket():
	# global cursor, connection

	connection = sqlite3.connect("./mp1.db")
	cursor = connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON;")
	connection.commit()

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

	return True