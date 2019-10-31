import sqlite3
import random
import time

def find_car_owner():
	# global cursor, connection

	connection = sqlite3.connect("./mp1.db")
	cursor = connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON;")
	connection.commit()
	# user provides one or more of make, model, year, color, and plate.
	
	# will concatenate at least one condition according to provided input
	finalQuery = '''select make, model, year, color, plate, regdate, expiry, fname, lname
	   				from registrations r join vehicles v using(vin) 
	   				where ''' 
	print()
	success = False
	while success == False:
		make = input("make: ")
		model = input("model: ")
		year = input("year: ")
		color = input("color: ")
		plate = input("plate: ")

		parameters = []
		if make != "":
			finalQuery += "make=? and "
			parameters.append(make)
			success = True
		if model != "":
			finalQuery += "model=? and "
			parameters.append(model)
			success = True
		if year != "":
			finalQuery += "year=? and "
			parameters.append(year)
			success = True
		if color != "":
			finalQuery += "color=? and "
			parameters.append(color)
			success = True
		if plate != "":
			finalQuery += "plate=? and "
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
			# finalQuery += ";"
			# print(finalQuery)

			cursor.execute(finalQuery, parameters)
			rows = cursor.fetchall()
			# print(rows)
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