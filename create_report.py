#!/usr/bin/env python3
import sys
from datetime import datetime
from dbconfig import read_db_config
from mysql.connector import Error, MySQLConnection


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
    L1 = [] 
    L2 = []
    L3 = []
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        
        #retrieve trans id, trans date, last 6 card number
        cursor.execute("SELECT LPAD(t.trans_id, 5, 0), DATE_FORMAT(t.trans_date, '%Y%m%d%h%i%s'),RIGHT(t.card_num,6) FROM trans t JOIN trans_line tl ON t.trans_id = tl.trans_id JOIN  products p ON p.prod_num = tl.prod_num WHERE t.trans_date > '%s' GROUP BY LPAD(t.trans_id, 5, 0), DATE_FORMAT(t.trans_date, '%Y%m%d%h%i%s'),RIGHT(t.card_num,6)",(bdate))   
        result = cursor.fetchall()
        
        #add each row to List L1
        for row in result:
            L1.append("{}{}{}".format(row[0],row[1],row[2]))
        
        #retrieve all product qty, amt, and description
        x = 1
        i = 0
        while x != 7:
            while i != 3:
                cursor.execute("SELECT RPAD(TRUNCATE(tl.qty,0),2,0), RIGHT(tl.amt,6), p.prod_desc, tl.trans_id FROM trans_line tl INNER JOIN products p ON tl.prod_num = p.prod_num WHERE tl.line_id = '%s' AND tl.trans_id = '%s' GROUP BY tl.qty, tl.amt, p.prod_desc, tl.trans_id",(i,x))
                prod = cursor.fetchall()
                if prod:
                    for row in prod:
                        #format to remove . and pad with zeros, add to list L2
                        newAmt = str(row[1]).replace(".","").zfill(6)
                        L2.append("{}{}{}".format(row[0],newAmt,row[2]))
                else:
                    L2.append("00000000")
                i += 1
            i = 0
            x += 1
        
        #retrieve all totals
        x = 1
        while x != 7:
            cursor.execute("SELECT total FROM trans WHERE trans_id = '%s'" % (x))
            total = cursor.fetchall()
            for item in total:
                #format and add to list L3
                newItem = str(item[0]).replace(".","").zfill(6)
                L3.append(newItem)
            x += 1
        
        #print each line
        x = 0
        i = 0
        t = 0
        while x != 6:
            line = ("{}{:<20} {:<20} {:<20} {:<20}".format(L1[x],L2[i],L2[i+1],L2[i+2],L3[t]))
            print(line)
            x += 1
            i += 3
            t += 1
        
            
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
