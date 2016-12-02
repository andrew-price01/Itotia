"""
"""
#!/usr/bin/env python3
import sys
import mysql.connector
from dbconfig import read_db_config
from mysql.connector import Error, MySQLConnection

def connect():
    """
    Connect to SQL DB with connect file.
    """
    db_config = read_db_config()
    try:
        print("Connecting to MySQL Database...")
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print("Connection Successful.")
        else:
            print("Connection Failed.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Trans")
        
        rows = cursor.fetchall()
        print("Total Row(s)")
        for row in rows:
            print(row)

        #row = cursor.fetchone() #select first row

        #while row is not None:
        #    print(row)
        #    row = cursor.fetchone() #select next row

    except Error as error:
        print(error)

    finally:
        conn.close()
        print("Connection Closed.")

#main function
def main():
    """
    Test function
    """
    connect()


if __name__ == "__main__":
    #Call Main
    main()

    exit(0)

