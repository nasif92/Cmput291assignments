import sqlite3
import random, datetime

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

# this one takes in table and executes and gives a unique key plus 1 the old one
def getUnique(table, key):
	global cursor, connection
	# this is for checking if a key is already present
	# probably not required
	cursor.execute("SELECT %s from %s;" %(key,table))
	all = cursor.fetchall()
	for x in all:
		print(x)
	#main functionality
	cursor.execute("SELECT %s FROM %s ORDER BY %s DESC limit 1;" %(key, table, key))
	num = cursor.fetchone()	
	for x in num:
		return x+1

#getting parents information like phone and address
def getParentInfo(fname, lname):
	global cursor, connection
	data = (fname, lname,)
	cursor.execute('''SELECT persons.address, persons.phone from persons, births
					WHERE births.m_fname = persons.fname AND births.m_lname = persons.lname
					AND births.fname = ? AND births.lname = ? ''' ,data)
	parent = cursor.fetchone()
	return parent

def getDate():
	now = datetime.datetime.now()
	date = now.strftime("%Y/%m/%d")
	return date

def main():
	global connection, cursor
	connect("./mp1.db")
	#sth = getUnique("births", "regno")
	#print(sth, x)

	#cursor.execute('''SELECT * from births''')
	#all = cursor.fetchall()
	#print(all)
	parent = getParentInfo("Nasif2","Hossain2")
	print(parent)
	
main()