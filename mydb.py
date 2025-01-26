import mysql.connector

try:
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='11111'
    )
    if dataBase.is_connected():
        print("Connection successful")

except Error as e:
    print(f"Error: {e}")

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a DataBase
cursorObject.execute("CREATE DATABASE django_crm_mysql_database")

print("All Done!!!")
