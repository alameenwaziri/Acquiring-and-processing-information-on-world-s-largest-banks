# Code for ETL operations on Country-GDP data

# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '8Y-%m-%d SH:%M:%5' # Year-Month-Day Hour:Minute:Second
    now = datetime.now() # Get the current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("code_log. txt", "a") as f:
        f.write(f"{timestamp} : {message}\n")


def extract(url, table_attribs):
    ''' The purpose of this function is to extract the required
    information from the website and save it to a dataframe. The
    function returns the dataframe for further processing. '''
    
    # Fetch the HTML content of the page
    page = requests.get(url).text
    # Parse the HTML content using BeautifulSoup
    data = BeautifulSoup(page, 'html.parser') 
    # Initialize the DataFrame with the provided column attributes
    df = pd.DataFrame(columns=table_attribs) 
    # Find all tables on the page
    tables = data.find_all('table', {'class': 'wikitable'})
    # Assuming that the correct table is the first "wikitable"
    table = tables[0]
    # Extract rows from the table
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 3:
            # Extract bank name and market capitalization
            name = cols[1].text.strip()
            market_cap = cols[2].text.strip().replace('\n', '').replace(',', '')
            
            if name and market_cap and '—' not in market_cap:
                data_dict = {"Name": name, "MC_USD_Billion": market_cap}
                df1 = pd.DataFrame([data_dict])
                df = pd.concat([df, df1], ignore_index=True)
    
    # Clean the Market Cap column
    df['MC_USD_Billion'] = df['MC_USD_Billion'].astype(float)
    
    return df


def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    
    # Read the exchange rate CSV file into a DataFrame
    exchange_rates_df = pd.read_csv(csv_path)
    
    # Convert the DataFrame into a dictionary
    exchange_rates = exchange_rates_df.set_index('Currency').to_dict()['Rate']

    # Add columns for Market Capitalization in different currencies
    df['MC_GBP_Billion'] = [np.round(x * exchange_rates.get('GBP', 1), 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rates.get('EUR', 1), 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rates.get('INR', 1), 2) for x in df['MC_USD_Billion']]
    
    return df

# Configure Pandas to display all columns
pd.set_option('display.max_columns', None)


def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    df.to_csv(output_path, index=False)  # Save DataFrame to the specified path


def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final DataFrame to a database
    table with the provided name. Function returns nothing. '''

    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


''' Here, define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

# Define the URL and table attributes
url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["Name", "MC_USD_Billion"]
# Define the path to the exchange rate CSV file
exchange_rate_csv_path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
# Define the database and table names
db_name = 'Banks.db'
table_name = 'Largest_banks'
# Define the output CSV path
output_csv_path = './Largest_banks_data.csv'
  

# Make the first log entry
log_progress('Preliminaries complete. Initiating ETL process')

# Call the extract function and store the result in df
df = extract(url, table_attribs)

# Log the completion of data extraction
log_progress("Data extraction complete. Initiating Transformation process")

# Call the transform function and store the result in df_transformed
df_transformed = transform(df, exchange_rate_csv_path)

# Log the completion of data transformation
log_progress("Data transformation complete. Initiating Loading process.")

load_to_csv(df, output_csv_path)

log_progress(f"Data saved to CSV file")

sql_connection = sqlite3.connect('Banks.db')

log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

# 1. Print the contents of the entire table
query_1 = f'SELECT * FROM Largest_banks'
run_query(query_1, sql_connection)

# 2. Print the average market capitalization of all the banks in Billion USD
query_2 = f'SELECT AVG(MC_GBP_Billion) FROM Largest_banks'
run_query(query_2, sql_connection)

# 3. Print only the names of the top 5 banks
query_3 = f'SELECT Name FROM Largest_banks LIMIT 5'
run_query(query_3, sql_connection)

log_progress('Process Complete.')

sql_connection.close()

log_progress('Server Connection closed.')
