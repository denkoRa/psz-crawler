import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="psz",
    password="123",
    database='discogs',
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()
mycursor.execute("SELECT name FROM genre")
#print(mycursor.fetchall())
for res in mycursor.fetchall():
    print (res)
