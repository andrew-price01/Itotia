#!/usr/bin/env python3
import sys
from datetime import datetime
from dbconfig import read_db_config
from mysql.connector import Error, MySQLConnection

#declare lists
transList = []
prodList = []
totalList = []

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
            print("Getting transaction from {} to {}".format(begTest,endTest))
            dateFormat(sys.argv[1],sys.argv[2])
            return False
        except ValueError:
            exit(-1)
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


def queryData(bdate, edate):
    """
    Description:
        Retrieve data from db
    Args:
        Begin date, end date.
    """
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        
        if conn.is_connected():
            print("Connected.")
        else:
            print("Connection Failed.")

        #retrieve trans id, trans date, last 6 card number
        cursor.execute("SELECT LPAD(trans_id, 5, 0), DATE_FORMAT(trans_date, '%Y%m%d%H%i'),RIGHT(card_num,6) FROM trans WHERE trans_date >= %s AND trans_date <= %s GROUP BY trans_id, trans_date, card_num",(bdate, edate))   
        result = cursor.fetchall()
 
        if result:

            #add each row to List transList
            for row in result:
                transList.append("{}{}{}".format(row[0],row[1],row[2]))
        
            #retrieve all product qty, amt, and description
            x = 1
            i = 0
            while x != len(transList) + 1:
                while i != 3:
                    cursor.execute("SELECT RPAD(TRUNCATE(tl.qty,0),2,0), RIGHT(tl.amt,6), p.prod_desc, tl.trans_id FROM trans_line tl INNER JOIN products p ON tl.prod_num = p.prod_num WHERE tl.line_id = %s AND tl.trans_id = %s GROUP BY tl.qty, tl.amt, p.prod_desc, tl.trans_id",(i,x))
                    prod = cursor.fetchall()
                    if prod:
                        for row in prod:
                            #format to remove . and pad with zeros, add to list prodList
                            newAmt = str(row[1]).replace(".","").zfill(6)
                            prodList.append("{}{}{}".format(row[0],newAmt,row[2]))
                    else:
                        prodList.append("00000000")
                    i += 1
                i = 0
                x +=1
            
            #retrieve all totals
            x = 1
            while x != len(transList) + 1:
                cursor.execute("SELECT total FROM trans WHERE trans_id = %s" % (x))
                total = cursor.fetchall()
                for item in total:
                    #format and add to list totalList
                    newItem = str(item[0]).replace(".","").zfill(6)
                    totalList.append(newItem)
                x += 1
        else:
            exit(-2)

    except Error as e:
        print(e)

    finally:
        createReport()
        cursor.close()
        conn.close()
        print("Disconnected.")

#Create fixed-length report, company_trans_begDate_endDate.dat
def createReport():
    """
    Description: 
        Create formatted report on data retrieved.
    Args:
        None.
    Return:
        Output .dat file
    """
    x = 0
    i = 0
    t = 0
    while x != len(transList):
        fname = ("company_trans_{}_{}.dat").format(sys.argv[1],sys.argv[2])
        line = ("{:<20}{:<20} {:<20} {:<20} {:>5}".format(transList[x],prodList[i],prodList[i+1],prodList[i+2],totalList[t]))
        with open(fname,"a") as myfile:
            myfile.write(line)
            myfile.write('\n')
        print("[{}]".format(line))
        x += 1
        i += 3
        t += 1


def main():
    """
    Description:
        Call getInput(), queryData(), and createReport().
    Args:
        None.
    """
    getInput()
    queryData(beg_date, end_date)

if __name__ == '__main__':
    #call main
    main() 

    exit(0)
