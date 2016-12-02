#!/usr/bin/env python3
import sys
from datetime import datetime
from dbconfig import read_db_config
from mysql_connect import Error, MySQLConnection


def getInput():
    """
    Description: 
        Check input arguments for correct date format. Exit -1 if error, Call dateFormat() if true.
    Args:
        None.
    """
    while True:
        try:
            begTest = sys.argv[1]
            endTest = sys.argv[2]
            begTest = datetime.strptime(begTest, '%Y%m%d')
            endTest = datetime.strptime(endTest,'%Y%m%d')
            dateFormat(sys.argv[1],sys.argv[2])
            return False
        except ValueError:
            exit -1
            break

def dateFormat(begDate,endDate):
    """
    Description: 
        Format input to date-time format.
    Args:
        Begin date, end date.
    """
    global beg_date, end_date;
    beg_date = datetime.strptime(begDate,'%Y%m%d').strftime('%Y-%m-%d 00:00')
    end_date = datetime.strptime(sys.argv[2],'%Y%m%d').strftime('%Y-%m-%d 23:59')
    #print("Beginning date: {}".format(beg_date))
    #print("Ending date: {}".format(end_date))


def connect():
    """
    Description:
        Connect to SQL DB with connect file.
    Args:
        None
    Returns:
        SQL Connection
    """
    db_config = read_db_config()
    try:
        print("Connecting to MySQL Database...")
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print("Connection Successful.")
        else:
            print("Connection Failed.")
    except Error as error:
        print(error)
    return conn

def disconnect(conn):
    """
    Description: 
        Disconnect a previously established SQL connection.
    Args:
        conn: a previously established connection.
    """
    conn.close()
    print("Connection Closed.")

def query_with_fetchone(bdate, edate):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        cursor.execute("SELECT LPAD(t.trans_id, 5, '0'), DATE_FORMAT(t.trans_date,'%Y%m%d%h%i%s'),RIGHT(t.card_num,6) FROM trans t JOIN trans_line tl ON t.trans_id = tl.trans_id JOIN products p ON p.prod_num = tl.prod_num WHERE t.trans_date > 2016-12-01 GROUP BY LPAD(t.trans_id,5,'0'), t.trans_date, RIGHT(t.card_num,6)")
        result = cursor.fetchall()
        
        for row in result:
            for i in row:
                print(i)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def main():
    getInput()
    query_with_fetchone(beg_date, end_date)
    

if __name__ == '__main__':
    #call main
    main() 

    exit(0)
