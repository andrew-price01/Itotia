#!/bin/bash - 
#===============================================================================
#
#         USAGE: ./run_report.sh 
# 
#   DESCRIPTION: 
# 
#        AUTHOR: Karl Marble (), karlmarble@mail.weber.edu
#  ORGANIZATION: 
#       CREATED: 12/02/2016 01:51
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

function reqHelp {
	echo "Usage is run_report.sh [-f BegDate] [-t EndDate] [-e email] [-u FTP username] [-p FTP password]"
	exit 1
}

if [ "$1" == "--help" ] || [ -z "$1" ]; then
	reqHelp
fi

while getopts ":f:t:e:u:p:" opt; do
	case $opt in
		f) beg_date=$OPTARG;;
		t) end_date=$OPTARG;;
		e) email=$OPTARG;;
		u) user=$OPTARG;;
		p) pass=$OPTARG;;
		\?) reqHelp;;
	esac
done


python3 ./create_report.py $beg_date $end_date

#exit code 0:
	#compress file with zip and transfer it via FTP to FTP server using FTP credentials
		# verify file is unzippable, send email to client Header: Successfully transfer file (FTP Address) 
		# Body: Successfully created a transaction report from BegDate to EndDate
case $? in
	0) exit 1 ;;

# exit code -1:
	# Email customer -  header: The create_report program exit with code -1 body: Bad Input parameters BegDate EndDate
	'-1') echo "Bad Input parameters BegDate EndDate" ;;

# exit code -2:
	# Email customer - header: The create_report program exit with code -2 body: No transactions available from BegDate to EndDate
	'-2') echo "No transactions available from BegDate to EndDate" ;;
esac

exit 0
