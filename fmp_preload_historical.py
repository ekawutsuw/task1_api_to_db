from dotenv import load_dotenv
import os
import requests
import pymysql

def main():
	''' GET ENVIRONMENT VARIABLES AND SECRETS '''
	load_dotenv() # Load .env
	dbhost = os.getenv('DBHOST', "")
	dbuser = os.getenv('DBUSER', "")
	dbpassword = os.getenv('DBPASSWORD', "")
	database = os.getenv('DATABASE', "")
	table = os.getenv('TABLE', "")

	''' CONNECT TO THE DATABASE '''
	connection = pymysql.connect(
		host=dbhost,
		user=dbuser,
		password=dbpassword,
		db=database)

	# Create cursor
	cursor = connection.cursor()
	
	symbol_list = ['AAPL', 'FB']

	# Create column list & SQL command
	cols = '`symbol`, `date`, `open`, `high`, `low`, `close`, `adjustment_close`, `volume`, `unadjusted_volume`, `change_value`, `change_percent`, `vwap`, `label`, `change_over_time`'
	sql = 'INSERT INTO `'+table+'` ('+cols +') VALUES ('+'%s,'*(13)+'%s)'

	''' RETRIEVE DATA VIA API '''
	for symbol in symbol_list:
		url = 'https://financialmodelingprep.com/api/v3/historical-price-full/'+symbol
		response = requests.get(url)
		
		json_data = response.json()
		for i in range(len(json_data['historical'])):
			# Create data tuple
			tuple_data = (symbol, json_data['historical'][i]['date'], json_data['historical'][i]['open'], json_data['historical'][i]['high'], json_data['historical'][i]['low'], json_data['historical'][i]['close'], json_data['historical'][i]['adjClose'], json_data['historical'][i]['volume'], json_data['historical'][i]['unadjustedVolume'], json_data['historical'][i]['change'], json_data['historical'][i]['changePercent'], json_data['historical'][i]['vwap'], json_data['historical'][i]['label'], json_data['historical'][i]['changeOverTime'])

			# Insert data records one by one.
			# print(sql % tuple_data)
			cursor.execute(sql, tuple_data)
		
			# The connection is not autocommitted by default, so we must commit to save our changes
			connection.commit()

	connection.close()

if __name__ == '__main__':
	main()
