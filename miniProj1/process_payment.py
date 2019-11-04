import sqlite3
import random
import datetime
import system
def process_payment():
	global connection, cursor,database
	cursor = system.cursor
	connection = system.connection


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


