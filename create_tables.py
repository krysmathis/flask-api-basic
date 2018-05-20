import sqlite3

# Creating the database
connection = sqlite3.connect('data.db')

# create the connection
cursor = connection.cursor()

# saving this for later
# drop_table = "DROP TABLE IF EXISTS items"

# cursor.execute(drop_table)

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# now run the sql
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
# now run the sql
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS areas (id INTEGER PRIMARY KEY, location text, locid int, capture_date DATE, image BLOB)"
# now run the sql
cursor.execute(create_table)

# # run queries
# delete_query = "DELETE FROM users"
# cursor.execute(delete_query)

# user = ('krys', 'asdf')
# insert_query = "INSERT INTO users (username, password) VALUES (?,?)"

# cursor.execute(insert_query, user)
# cursor.execute("INSERT INTO items VALUES (NULL, 'test', 9.99)")

area = ('location1', 1, '2018-05-20', '01010101')
insert_query = ("INSERT INTO areas VALUES (NULL, ?, ?, ?, ?);")
cursor.execute(insert_query, area)

# users = [
#     ('rolf', 'asdf'),
#     ('anne', 'xyz')
# ]

# cursor.executemany(insert_query, users)

# select_query = "SELECT * FROM users"
# for row in cursor.execute(select_query) :
#     print(row)

connection.commit()
connection.close()