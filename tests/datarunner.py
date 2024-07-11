#!/usr/bin/python3
"""
This script connects to a MySQL database and selects all the rows from the 'states' table.
"""

import sys
import MySQLdb as mysql

if __name__ == "__main__":
    mysql_username = sys.argv[1]
    mysql_password = sys.argv[2]
    database_name = sys.argv[3]

    db = mysql.connect(
        host="localhost",
        port=3306,
        user=mysql_username,
        password=mysql_password,
        db=database_name
    )

    cursor = db.cursor()
    cursor.execute("SELECT * FROM states ORDER BY id ASC")
    result = cursor.fetchall()

    for x in result:
        print(x)
