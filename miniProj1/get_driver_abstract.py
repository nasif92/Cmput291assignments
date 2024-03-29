import sqlite3
import random, datetime
from person_class import createPerson, getPerson, getDate, getUnique
import system


def get_driver_abstract():
	global connection, cursor,database
	cursor = system.cursor
	connection = system.connection

	given =False
	quit = False

	while not given:
		prompt = ""
		fname = input("Enter fname: ")
		lname = input("Enter lname: ")
		if fname == "" or lname == "":
			print("Please input both first name and last name")
		if getPerson(fname,lname):
			given = True
		else:
			prompt = input ("Person named %s %s is not in database. Press q to quit: " %(fname, lname))
			if prompt == "q":
				quit = True
				print()
			given = True

	if given and not quit:
		cursor.execute('''SELECT count(DISTINCT tno) as got_tickets , COUNT(distinct demeritNotices.ddate) AS NOTICES
							from demeritNotices left outer join registrations using (fname,lname)
							left outer join tickets using (regno)
							WHERE date(demeritNotices.ddate) >= date('now','-2 years') 
							AND fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP BY fname, lname''',(fname,lname))
		data_2years = cursor.fetchone()
		cursor.execute('''SELECT count(DISTINCT tno) as got_tickets , COUNT(distinct demeritNotices.ddate) AS NOTICES
							from demeritNotices left outer join registrations using (fname,lname)
							left outer join tickets using (regno)
							WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP BY fname, lname''',(fname,lname))
		data_lifetime = cursor.fetchone()
		cursor.execute('''SELECT sum(demeritNotices.points) FROM demeritNotices
							WHERE date(ddate) >= date('now','-2 years')
							AND fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP by fname, lname''',(fname,lname,))
		points_2years = cursor.fetchone()
		cursor.execute('''SELECT sum(demeritNotices.points) FROM demeritNotices
							WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
							GROUP by fname, lname''',(fname,lname,))
		points_lifetime = cursor.fetchone()
		cursor.execute('''SELECT tno, vdate,violation,fine,regno, make, model
							from (SELECT * from tickets
								left outer join registrations using (regno)
								left outer JOIN vehicles USING (vin)
								ORDER by vdate DESC
								)
								WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE''',(fname,lname,))
		tickets = cursor.fetchall()
		print(30*"=")

		print("Name: %s %s" %(fname.capitalize(),lname.capitalize()))
		print(30*"=")

		print("Over the last two years: ")
		print("Number of tickets: %s \nNumber of demerit notices: %s\nTotal number of demerit points: %s" %(data_2years[0],data_2years[1],points_2years[0]))
		print(30*"=")
		print("Over the lifetime of %s %s: " %(fname.capitalize(),lname.capitalize()))
		print("Number of tickets: %s \nNumber of demerit notices: %s\nTotal number of demerit points: %s" %(data_lifetime[0],data_lifetime[1],points_lifetime[0]))
		print(30*"=")
		print("All 5 latest tickets from in sorted order from latest to oldest: ")
		print(30*"=")
		i = 0
		if len(tickets) == 0:
			print("None")
		else:
			while i < 5 and i < len(tickets):
				print("ticket number: %s, violation date: %s \nviolation description: %s, fine: %s, registration number: %s \nmake: %s, model of car: %s" %(tickets[i][0],tickets[i][1],tickets[i][2],tickets[i][3],tickets[i][4],tickets[i][5],tickets[i][6])) 
				print(30*"=")
				i += 1
			if  len(tickets) > 5:
				prompt = input("Would you like to see more?: (y/n)")
				if prompt is "y" or prompt is "Y":
					while i < len(tickets):
						print("ticket number: %s, violation date: %s \nviolation description: %s, fine: %s, registration number: %s \nmake: %s, model of car: %s" %(tickets[i][0],tickets[i][1],tickets[i][2],tickets[i][3],tickets[i][4],tickets[i][5],tickets[i][6])) 
						print(30*"=")
						i+= 1
	print("\nExiting!\n")

