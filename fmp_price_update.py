from dotenv import load_dotenv
import os
import requests
import pymysql

import datetime
from dateutil import tz

def main():
	''' DATETIME '''
	utc_time_zone = tz.gettz('UTC')
	# th_time_zone = tz.gettz('Asia/Bangkok')
	current_datetime = datetime.datetime.now(utc_time_zone) # DATETIME OBJECT
	current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S') # STRING
	current_date_str = current_datetime.strftime('%Y-%m-%d') # STRING
	# print(current_datetime_str)
	# print(current_date_str)

	'''	The stock market is not open on weekends!
		weekday() = 5 means Saturday and weekday() = 6 means Sunday
	'''
	if current_datetime.weekday()>4:
		# print('Weekend!')
		return
	
	''' GET ENVIRONMENT VARIABLES AND SECRETS '''
	load_dotenv() # Load .env
	dbhost = os.getenv('DBHOST', "")
	dbuser = os.getenv('DBUSER', "")
	dbpassword = os.getenv('DBPASSWORD', "")
	database = os.getenv('DATABASE', "")
	table = os.getenv('FMPTABLE', "")

	''' CONNECT TO THE DATABASE '''
	connection = pymysql.connect(
		host=dbhost,
		user=dbuser,
		password=dbpassword,
		db=database)

	# Create cursor
	cursor = connection.cursor()

	symbol_list = ['AAPL', 'FB']

	''' RETRIEVE DATA VIA API '''
	for symbol in symbol_list:
		# Check if the data point exists
		is_found = False
		select_sql = 'SELECT * FROM `'+table+'` WHERE `symbol`=\''+symbol+'\' AND `date`=\''+current_date_str+'\''
		cursor.execute(select_sql)
		# Fetch all the records
		results = cursor.fetchall()
		for row in results:
			is_found = True
			# print(row)

		url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/'+symbol
		response = requests.get(url)
		json_data = response.json()

		if is_found:
			# Create SQL command for real-time price update
			update_sql = 'UPDATE `'+table+'` SET `real_time_price`=%s, `last_updated`=\''+current_datetime_str+'\' WHERE `symbol`=%s AND `date`=\''+current_date_str+'\''

			# Create data tuple
			tuple_data = (json_data['price'], symbol)

			# Update data records one by one.
			# print(update_sql % tuple_data)
			cursor.execute(update_sql, tuple_data)
		
			# The connection is not autocommitted by default, so we must commit to save our changes
			connection.commit()

		else:
			# Create SQL command for real-time price insert
			cols = '`symbol`, `date`, `real_time_price`, `last_updated`'
			insert_sql = 'INSERT INTO `'+table+'` ('+cols +') VALUES ('+'%s,'*(3)+'%s)'

			# Create data tuple
			tuple_data = (symbol, current_date_str, json_data['price'], current_datetime_str)

			# Insert data records one by one.
			# print(insert_sql % tuple_data)
			cursor.execute(insert_sql, tuple_data)

			connection.commit()
	
	connection.close()

if __name__ == '__main__':
	main()
