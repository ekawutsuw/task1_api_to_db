INSERT INTO mysql.user (User,Host,authentication_string,ssl_cipher,x509_issuer,x509_subject) VALUES('demouser','localhost',PASSWORD('demopassword'),'','','');
FLUSH PRIVILEGES;
SELECT User, Host, authentication_string FROM mysql.user;

CREATE DATABASE IF NOT EXISTS financial_database;
USE financial_database;

DROP TABLE IF EXISTS financial_modeling_prep;
CREATE TABLE financial_modeling_prep ( fmp_id int unsigned not null auto_increment, symbol varchar(10), date date, open float, high float, low float, close float, adjustment_close float, volume float, unadjusted_volume float, change_value float, change_percent float, vwap float, label varchar(128), change_over_time float, real_time_price float, last_updated datetime, primary key (fmp_id) );