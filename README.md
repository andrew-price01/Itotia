# Itotia_hw8
(Module 1: config.ini) Set your environment variables. This module will set all your
  variables needed to connect to the DB. Modify the code below to match
  credentials.

(Module 2: create_report.py) This takes two input parameters (beg_date, end_date).
  two parameters, which are needed to query your database, are being input with
  following format: YYYYMMDD. With this information, you will query your DB to
  the transaction information needed for your report.
      
(Script 1: run_report.sh) Create a shell wrapper script that will call your create_report.py
  module.

Setting MySQL Data: For this project, you need to load the following information into
your DB:
  a. Copy Data: $ cp /home/hvalle/submit/cs3030/files/hw8.sql .
  b. Load Data: $ mysql –u USER –p –D DATABASE < hw8.sql
