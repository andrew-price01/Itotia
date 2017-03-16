#!/bin/bash - 
#===============================================================================
#
#         USAGE: ./run_report.sh 
# 
#   DESCRIPTION: runs a python3 script that takes the date arguments from this 
#		script to parse a sql file. it then compresses the file using zip and 
#		using and FTP connection places it in the customer_server/ folder on a
#		remote server then emails the user of file transfer
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

#check exit codes
code=$?
#exit code 0:
	#compress file with zip and transfer it via FTP to FTP server using FTP credentials
		# verify file is unzippable, send email to client Header: Successfully transfer file (FTP Address) 
		# Body: Successfully created a transaction report from BegDate to EndDate
if [ "$code" == "0" ]; then
	#set FTP variables
	HOST='137.190.19.105'
	USER=$user
	PASSWD=$pass
	#set file variables
	file="company_trans_"$beg_date"_"$end_date".dat"
	zipfile="company_trans_"$beg_date"_"$end_date".dat.zip"
	#compress file using zip
	zip $zipfile $file
	#put the compressed file in customer_server
	ftp -n $HOST <<-EoS
	user $USER $PASSWD
	cd customer_server
	put $zipfile
	quit
	EoS

	#send a mail stating the successful ftp of file
	mail -s "Successfully transfered file to FTP Server." "$email" <<-EoF
	Successfully created a transaction report from BegDate to EndDate
	EoF

# exit code -1:
	# Email customer -  header: The create_report program exit with code -1 body: Bad Input parameters BegDate EndDate
elif [ "$code" == "-1" ]; then
	mail -s "The create_report program exit with code -1" "$email" <<-EOF
	Bad Input parameters BegDate EndDate
	EOF
# exit code -2:
	# Email customer - header: The create_report program exit with code -2 body: No transactions available from BegDate to EndDate
elif [ "$code" == "-2" ]; then
	mail -s "The create_report program exit with code -2" "$email" <<-EOF
	No transactions available from BegDate to EndDate
	EOF
fi

exit 0
