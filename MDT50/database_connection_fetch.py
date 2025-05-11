import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="Test",
    user="postgres",
    password="123"
)
cursor = connection.cursor()
# #cursor.execute("SELECT * FROM your_table_name")
# cursor.execute("select version()")
# output = cursor.fetchall()
# #output = cursor.fetchone
# print (output)

try:
    cursor.execute("SELECT * FROM employee")

    # Fetch all results
    rows = cursor.fetchall()

    # Print each row
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print("Database error:", e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()