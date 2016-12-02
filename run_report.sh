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

while getopts ":f:t:e:u:p:"; do
	case $opt in
		f) beg_date=$OPTARG;;
		t) end_date=$OPTARG;;
		e) email=$OPTARG;;
		u) user=$OPTARG;;
		p) pass=$OPTARG;;
		\?) reqHelp;;
	esac
done

echo $beg_date
echo $end_date

#python3 ./create_report2.py $beg_date $end_date

exit 0

