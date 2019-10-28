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
	cursor.execute("SELECT %s FROM %s ORDER BY %s DESC limit 1;" %(key, table, key))
	num = cursor.fetchone()	
	for x in num:
		return x+1

def getDate():
	now = datetime.datetime.now()
	date = now.strftime("%Y/%m/%d")
	return date

def main():
	global connection, cursor
	connect("./mp1.db")
	sth = getUnique("births", "regno")
	x = getDate()
	print(sth, x)
main()