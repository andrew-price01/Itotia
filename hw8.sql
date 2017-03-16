# profile2.sql

DROP TABLE IF EXISTS trans;
--#@ _CREATE_TABLE_
CREATE TABLE trans
(
  trans_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  trans_date  TIMESTAMP,
  card_num  VARCHAR(25),
 total		float(9,2),
  PRIMARY KEY (trans_id)
);
--#@ _CREATE_TABLE_

INSERT INTO trans
  VALUES
    (NULL,NULL, "40000000507889", 100.00),
    (NULL,NULL, "40000000507888", 110.00),
    (NULL,NULL, "40000000507885", 140.00),
    (NULL,NULL, "30000000407280", 50.00),
    (NULL,NULL, "30000000407231", 40.00),
    (NULL,NULL, "30000000407229", 10.00)
;

DROP TABLE IF EXISTS trans_line;
--#@ _CREATE_TABLE_
CREATE TABLE trans_line
(
  trans_id    INT,
  line_id     INT,
  prod_num INT,
  qty		 float(9,2),
  amt        float(10,2),
  PRIMARY KEY (trans_id, line_id)
);
--#@ _CREATE_TABLE_

INSERT INTO trans_line
  VALUES
	(1,0,1,30.5, 90.0),
	(1,1,2,5.0, 10.0),
	(2,0,1,45.0, 110.0),
	(3,0,1,10.0, 50.0),
	(3,1,3,1.0, 30.0),
	(3,2,5,1.0, 60.0),
	(4,0,1,10.0, 50.0),
	(5,0,3,20.0, 40.0),
	(6,0,2,1.0, 7.50),
	(6,1,4,1.0, 1.50),
	(6,2,3,1.0, 1.00)
	;


DROP TABLE IF EXISTS products;
--#@ _CREATE_TABLE_
CREATE TABLE products
(
  prod_num   INT, 
  prod_desc  CHAR(20),
  PRIMARY KEY (prod_num)
);
INSERT INTO products
  VALUES
	(1,"FUEL"),
	(2,"MILK"),
	(3,"EGGS"),
	(4,"BREAD"),
	(5,"BEER");
