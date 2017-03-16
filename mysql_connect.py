#!/usr/bin/env python3
import sys
from dbconfig import read_db_config
from mysql.connector import Error, MySQLConnection

def connect(bDate, eDate):
    
    db_config = read_db_config()

    try:
        print("Connecting to MySQL database..")
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print("Connection Established.")
        else:
            print("Connected Failed")

            cursor - conn.cursor()
            cursor.execute("SELECT * FROM products p, trans t, trans_line t1 WHERE p.prod_num = t1.prod_num AND t1.trans_id = t.trans_id AND t.trans_date BETWEEN %s AND %s ORDER BY t.trans_date", (bDate, eDate))

            contents = list(cursor.fetchall())

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
        print("Connection Close")
        if contents is not None:
            print("Here's the data")
            return contents

def main():
    connect()
    pass

if __name__ == "__main__":
    main()
    exit(0)
