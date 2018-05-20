import sqlite3

def create_db() : 
    # Creating the database
    connection = sqlite3.connect('data.db')

    # create the connection
    cursor = connection.cursor()

    # saving this for later
    # drop_table = "DROP TABLE IF EXISTS areas"

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

    # check if location1 exists and if not
    query = "SELECT * FROM areas WHERE location=?"
    # parameters have to be in a tuple
    result = cursor.execute(query, ("location1",))
    row = result.fetchone()

    if row is None:
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