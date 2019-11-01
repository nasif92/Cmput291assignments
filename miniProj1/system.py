import sqlite3
import random
import time
import datetime

import issue_ticket
import find_car_owner
import Billofsale
import process_payment
import register_marriage
import renew_registration
import register_birth
import get_driver_abstract

connection = None
cursor = None
city = ""

def main():
	global connection, cursor
	connection = sqlite3.connect("./mp1.db")
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

		# prompt = input("Press enter to continue, or q to close the program: ")
		
	

def login_screen():
	##### must counter SQL injection attacks and make the password non-visible at the time of typing! #####
	global city

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
		
		cursor.execute("select utype, city from users where uid=? and pwd=?", (uid, pwd))
		rows = cursor.fetchall()
		if not rows:
			print("The User Id and Password combination did not return any results.")
		else:
			valid = True
			utype = rows[0][0]
			city = rows[0][1]
			# print(city)

	return utype


def operation_choice(user_type):
	# The operations are different for each user type

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
				register_birth.register_a_birth(city)
			elif choice == "2":
				register_marriage.register_marriage(city)
			elif choice == "3":
				renew_registration.renew_registration()
			elif choice == "4":
				Billofsale.bill_of_sale()
			elif choice == "5":
				process_payment.process_payment()
			elif choice == "6":
				get_driver_abstract.get_driver_abstract()
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
				issue_ticket.issue_ticket()
			elif choice == "2":
				find_car_owner.find_car_owner()
			elif choice == "l":
				print("\nYou have logged out.\n")
				complete = True
				# break

	return True


main()