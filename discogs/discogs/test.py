import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="psz",
    password="123",
    database='discogs',
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM style")
# res = mycursor.fetchall()
# print(res)
style = 'Folk, World, & Country'
val = {"name": style }
insert_style = "INSERT INTO style(name) VALUES (%(name)s)"
mycursor.execute(insert_style, val)
mydb.commit()
print(mycursor.rowcount, "records inserted")