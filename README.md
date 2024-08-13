# Acquiring-and-processing-information-on-world-s-largest-banks
Acquiring and processing information on world's largest banks

Here is an industry-grade README file for your data engineering project. This README will provide a comprehensive overview of the project, including setup instructions, usage, and other essential details.

---

# README: Largest Banks Data Engineering Project

## Project Overview

This project involves creating an automated system to extract, transform, and load (ETL) data about the top 10 largest banks in the world, ranked by market capitalization. The data will be extracted from a webpage, transformed to include additional currency values, and then loaded into both a CSV file and an SQL database.

## Project Structure

- `banks_project.py`: Main Python script implementing the ETL process.
- `Largest_banks_data.csv`: Output CSV file containing the final data.
- `Banks.db`: SQLite database file containing the data.
- `code_log.txt`: Log file for tracking the progress of the script.

## Prerequisites

Ensure you have the following libraries installed:

- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `sqlite3` (part of the Python standard library)
- `datetime`

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4 pandas numpy
```

## Functionality

### 1. Data Extraction

**Function**: `extract(url, table_attribs)`

- **Purpose**: Extract data from a webpage about the largest banks by market capitalization.
- **Input**: 
  - `url`: URL of the webpage.
  - `table_attribs`: List of table attributes to extract.
- **Output**: DataFrame containing bank names and market capitalization in USD.

### 2. Data Transformation

**Function**: `transform(df, csv_path)`

- **Purpose**: Transform the extracted data to include market capitalization in GBP, EUR, and INR based on provided exchange rates.
- **Input**: 
  - `df`: DataFrame from the `extract` function.
  - `csv_path`: Path to the exchange rate CSV file.
- **Output**: Transformed DataFrame with additional columns for market capitalization in GBP, EUR, and INR.

### 3. Load to CSV

**Function**: `load_to_csv(df, output_path)`

- **Purpose**: Save the transformed DataFrame to a CSV file.
- **Input**: 
  - `df`: Transformed DataFrame.
  - `output_path`: Path where the CSV file will be saved.
- **Output**: CSV file containing the final data.

### 4. Load to Database

**Function**: `load_to_db(df, sql_connection, table_name)`

- **Purpose**: Load the transformed DataFrame into an SQL database.
- **Input**: 
  - `df`: Transformed DataFrame.
  - `sql_connection`: SQLite3 database connection object.
  - `table_name`: Name of the table to store the data.
- **Output**: Data stored in the specified database table.

### 5. Run Queries

**Function**: `run_query(query_statement, sql_connection)`

- **Purpose**: Execute SQL queries on the database and print the results.
- **Input**: 
  - `query_statement`: SQL query string.
  - `sql_connection`: SQLite3 database connection object.
- **Output**: Query results printed to the terminal.

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:

   ```bash
   pip install requests beautifulsoup4 pandas numpy
   ```

3. **Configure the Script**:

   Ensure the following variables in the script are correctly set:
   - `data_url`: URL of the webpage containing the bank data.
   - `exchange_rate_csv_path`: Path to the CSV file with exchange rates.
   - `output_csv_path`: Path where the final CSV will be saved.
   - `database_name`: SQLite database file name.
   - `table_name`: Name of the table in the database.

4. **Run the Script**:

   ```bash
   python banks_project.py
   ```

## Log File

The progress of the ETL process is logged in `code_log.txt`. This file will include entries for each stage of the process, such as extraction, transformation, and loading.

## Troubleshooting

- **File Not Found**: Ensure that file paths and URLs are correct.
- **Permission Issues**: Run the script with the necessary permissions or adjust file permissions as needed.
- **Dependencies**: Ensure all required libraries are installed.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any issues or inquiries, please contact:

- **Name**: [Your Name]
- **Email**: [Your Email]

---

Feel free to adjust the content to better fit your needs or to include any additional information relevant to your project.
