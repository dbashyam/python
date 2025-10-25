import psycopg2
connection = psycopg2.connect(
    host = "postgresdb.cjmu2mycww8n.ap-south-1.rds.amazonaws.com",
    user = "postgres",
    password = "rootpassword",
    port = 5432,
    database = 'vasanthdb'
)

cursor = connection.cursor()

#list all the database
# cursor.execute("select * from pg_database")

# cursor.fetchall()

cursor.execute("commit")

cursor.execute("create database vasanthdb")

cursor.execute("select * from california_housing")

cursor.fetchall()