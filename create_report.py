#!/usr/bin/env python3
import sys
from datetime import datetime
import dbconfig

def getInput():
    while True:
        try:
            begTest = sys.argv[1]
            endTest = sys.argv[2]
            begTest = datetime.strptime(begTest, '%Y%m%d')
            endTest = datetime.strptime(endTest,'%Y%m%d')
            dateFormat(sys.argv[1],sys.argv[2])
            return False
        except ValueError:
            print('Invalid date!')
            exit(-1)
            break

def dateFormat(begDate,endDate):
    beg_date = datetime.strptime(begDate,'%Y%m%d').strftime('%Y-%m-%d 00:00')
    end_date = datetime.strptime(sys.argv[2],'%Y%m%d').strftime('%Y-%m-%d 23:59')
    print("Beginning date: {}".format(beg_date))
    print("Ending date: {}".format(end_date))
       
def main():
    getInput()
    dbconfig.main()
if __name__ == '__main__':
    #call main
    main() 

    exit(0)
