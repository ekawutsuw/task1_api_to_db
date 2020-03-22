# Task1 API to Database

This is the project to demonstrate the ETL pipeline and how to import the data retrieved from the Financial Modeling Prep API to the MySQL database.

API Documentation: https://financialmodelingprep.com/developer/docs/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and the Python libraries.

The Python libraries listed in requirements.txt
```
python-dotenv==0.12.0
PyMySQL==0.9.3
requests==2.23.0
python-dateutil==2.8.1
```

### Installing

How to install them step by step.

```
sudo apt-get update
sudo apt-get install mysql-server

sudo apt install python3-pip
pip3 install -r requirements.txt
```

Then run the database script (db_script.sql) to create the user, the database, and the database table.

## Running the pipeline

There are two python files: fmp_preload_historical.py and fmp_price_update.py.

This fmp_preload_historical.py file should be executed manually first to load all the historical data into the database. This file retrieves data from the API, e.g. https://financialmodelingprep.com/api/v3/historical-price-full/AAPL.

```
python3 fmp_preload_historical.py
```

For the other file, fmp_price_update.py, the programme retrieves the real-time price from the API, e.g. https://financialmodelingprep.com/api/v3/stock/real-time-price/AAPL. This is to update the real-time price in the database every 2 minutes and 30 seconds.

```
crontab -e
```

Go to the last line, copy the command below and paste there. This cron command is to execute the programme every 2 minutes and 30 seconds. Reminder: replace the path to python file.

```
*/5 * * * * python3 /path/to/task1_api_to_db/fmp_price_update.py
*/5 * * * * (sleep 150; python3 /path/to/task1_api_to_db/fmp_price_update.py)
```

For the fmp_price_update.py programme, the new data loading in the database after pre-loading the historical data will have some missing fields from the API, /api/v3/historical-price-full.

Hence, there should be another programme to run every midnight in order to update the historical data day by day and to fill the missing data.
