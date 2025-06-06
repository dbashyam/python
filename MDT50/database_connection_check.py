import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="Test",
    user="postgres",
    password="123"
)
cursor = connection.cursor()
#cursor.execute("SELECT * FROM your_table_name")
cursor.execute("select version()")
output = cursor.fetchall()
#output = cursor.fetchone
print (output)