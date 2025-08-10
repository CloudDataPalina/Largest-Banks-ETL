# %pip install requests beautifulsoup4 pandas numpy matplotlib


# === Importing required libraries ===

import pandas as pd                    # For working with tables and CSV files
import numpy as np                     # For mathematical operations (e.g., rounding)
import requests                        # For downloading HTML pages from a website
from bs4 import BeautifulSoup          # For parsing HTML and web scraping tables
import sqlite3                         # For working with SQLite databases
from datetime import datetime          # For logging with timestamps
import matplotlib.pyplot as plt        # For data visualization


# === Set project parameters ===

#  Data source (web scraping)
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'       # Source of the table
table_attribs = ["Name", "MC_USD_Billion"]              # Columns to extract: Bank Name and Market Capitalization (in billions USD)

#  Paths to auxiliary files
exchange_rate_path = 'data/exchange_rate.csv'           # Path to the CSV file with currency exchange rates
log_path = './output/code_log.txt'                      # Path to the log file

#  Output paths
csv_path = './output/Largest_banks_data.csv'            # Path to the output CSV file
db_name = 'Banks.db'                                    # SQLite database name
table_name = 'Largest_banks'                            # Table name in the database


def log_progress(message):
    '''
    This function writes the given message to the log file
    using the current timestamp. It is used to track
    the stages of the ETL process execution.
    '''

    timestamp_format = '%Y-%b-%d-%H:%M:%S'                # Timestamp format: Year-Month-Day-Hour-Minute-Second
    now = datetime.now()                                  # Get the current date and time
    timestamp = now.strftime(timestamp_format)            # Convert timestamp to the required string format

    with open(log_path, "a") as f:                        # Open the log file in append mode
        f.write(timestamp + ' : ' + message + '\n')       # Write in the format: <time> : <message>



def extract(url, table_attribs):
    """
    Extracts a table of the largest banks from a Wikipedia page.
    
    Parameters:
    - url: link to the (archived) Wikipedia page
    - table_attribs: list of column names for the resulting DataFrame

    Returns:
    - df: DataFrame with two columns — Name and MC_USD_Billion
    """
    
    page = requests.get(url).text                              # Load the HTML content of the page from the given URL
    data = BeautifulSoup(page, 'html.parser')                  # Parse the HTML using the 'html.parser'
    
    df = pd.DataFrame(columns=table_attribs)                   # Create an empty DataFrame with the given columns
    
    tables = data.find_all('tbody')                            # Find all <tbody> elements — tables are usually inside them
    rows = tables[0].find_all('tr')                            # Extract rows from the first table (assuming it's the one we need)
    
    for row in rows:
        col = row.find_all('td')                               # Find all table cells (<td>) in the row
        if len(col) != 0:                                      # Skip rows without data (e.g., header rows)
            data_dict = {
                "Name": col[1].get_text(strip=True),           # Bank name — in the 2nd column
                "MC_USD_Billion": col[2].get_text(strip=True)  # Market cap — in the 3rd column
            }
            df1 = pd.DataFrame(data_dict, index=[0])           # Convert the dictionary to a DataFrame row
            df = pd.concat([df, df1], ignore_index=True)       # Append the row to the main DataFrame
    
    return df                                                  # Return the final DataFrame


def transform(df, exchange_rate_path):
    """
    Reads currency exchange rates from a CSV file,
    converts the MC_USD_Billion column into other currencies,
    and adds new columns with the converted values.
    """
    
    # Read the exchange rates file and create a dictionary: {'GBP': 0.8, 'EUR': 0.93, 'INR': 82.95}
    exchange_df = pd.read_csv(exchange_rate_path)                        # Load CSV with exchange rates
    exchange_rate = exchange_df.set_index('Currency').to_dict()['Rate']  # Convert to dict {currency: rate}

    # Convert the market capitalization column to float
    df['MC_USD_Billion'] = df['MC_USD_Billion'].astype(float)

    # Add a column with capitalization in GBP
    df['MC_GBP_Billion'] = [np.round(x * exchange_rate['GBP'], 2) for x in df['MC_USD_Billion']]

    # Add a column with capitalization in EUR
    df['MC_EUR_Billion'] = [np.round(x * exchange_rate['EUR'], 2) for x in df['MC_USD_Billion']]

    # 🇮🇳 Add a column with capitalization in Indian rupees (INR)
    df['MC_INR_Billion'] = [np.round(x * exchange_rate['INR'], 2) for x in df['MC_USD_Billion']]

    return df            # Return the updated DataFrame


def load_to_csv(df, csv_path):
    ''' 
    Saves the final DataFrame to a CSV file at the specified path.
    No return value.
    '''
    df.to_csv(csv_path, index=False)        # Save the table to CSV without indexes


def load_to_db(df, sql_connection, table_name):
    ''' 
    This function saves the final DataFrame into a database table 
    with the specified name. No value is returned.
    '''
    # Save the DataFrame into the database table (overwrite if exists, exclude index)
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    """ 
    Executes an SQL query on the database table and displays the result.
    No return value.
    """
    print(f"Running query: {query_statement}")               # Show the query being executed
    output = pd.read_sql(query_statement, sql_connection)    # Run the query and get a DataFrame
    print(output)                                            # output result


# === ETL ===

#  Logging the start of the ETL process
log_progress('Preliminaries complete. Initiating ETL process')

#  Step 1: Data Extraction (Extract)
df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process')

#  Step 2: Data Transformation (Transform)
df = transform(df, exchange_rate_path)
log_progress('Data transformation complete. Initiating loading process')

#  Step 3: Saving data to CSV
load_to_csv(df, csv_path)
log_progress('Data saved to CSV file')

#  Step 4: Connecting to SQLite database
sql_connection = sqlite3.connect('Banks.db')
log_progress('SQL Connection initiated.')

#  Step 5: Loading data into the database (Load)
load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as a table, Executing queries')

#  Step 6: Executing SQL queries
# 1. Display the entire table
query_statement = "SELECT * FROM Largest_banks"
run_query(query_statement, sql_connection)

# 2. Calculate the average market capitalization in GBP
query_statement = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query_statement, sql_connection)

# 3. Retrieve the first 5 bank names
query_statement = "SELECT Name FROM Largest_banks LIMIT 5"
run_query(query_statement, sql_connection)

#  Step 7: Process completion
log_progress('Process Complete.')

#  Closing the database connection
sql_connection.close()
log_progress('Server Connection closed.')


# ========= Connect to the SQLite database=========

# Connect to the SQLite database and automatically close after use
with sqlite3.connect("Banks.db") as conn:
    print("Connected to database successfully.")
    
    # SQL query to select the TOP 5 banks by USD market capitalization
    query = """
    SELECT Name, MC_USD_Billion, MC_GBP_Billion, MC_EUR_Billion
    FROM Largest_banks
    ORDER BY MC_USD_Billion DESC
    LIMIT 5
    """
    
    # Load the result into a DataFrame
    top5_simple = pd.read_sql(query, conn)
    print("Query executed successfully.")

# Save to CSV
top5_simple.to_csv("output/top5_banks.csv", index=False)
print("Data saved to output/top5_banks.csv")

print(top5_simple)




# ======== Building the bar chart=========
# Color palette for the three currencies:
colors = ['#0052cc', '#00b8d9', '#36B37E']  

#  Create a Figure and Axes object with a white background
fig, ax = plt.subplots(figsize=(9, 5), facecolor='white')  
ax.set_facecolor('white')                                   # set the background color of the plotting area

#  Building the bar chart:
#  Plot a bar chart with specified colors and black borders
top5_simple.set_index("Name")[["MC_USD_Billion", "MC_EUR_Billion", "MC_GBP_Billion"]].plot(
    kind='bar',                # chart type — vertical bars
    ax=ax,                     # axis to plot on
    color=colors,              # colors of the bars
    edgecolor='black',         # color of the bar borders
    linewidth=1                # border thickness
)

#  Title and axis labels
ax.set_title("Market Capitalization in USD, EUR, and GBP (Top 5 Banks)", 
             fontsize=16, fontweight='bold', color='black')                 # chart title
ax.set_ylabel("Market Capitalization (in billions)", fontsize=13, color='black')  # Y-axis label
ax.set_xlabel("")                                                           # remove X-axis label (banks are on tick labels)
ax.tick_params(axis='x', labelrotation=15, labelsize=11, colors='black')    # format X-axis ticks
ax.tick_params(axis='y', labelsize=11, colors='black')                      # format Y-axis ticks

#  Grid for better readability
ax.grid(axis='y', linestyle='--', color='gray', linewidth=0.8, alpha=0.9)   # horizontal grid
ax.grid(axis='x', linestyle=':', color='gray', linewidth=0.6, alpha=0.7)    # vertical grid

#  Frame styling (chart borders)
for spine in ax.spines.values():
    spine.set_edgecolor('black')                                            # black border
    spine.set_linewidth(1.2)                                                # border thickness

#  Legend with the title "Currency"
ax.legend(["USD", "EUR", "GBP"], title="Currency", title_fontsize=12, fontsize=11)

#  Save the chart as an SVG file (high quality, scalable)
plt.tight_layout()                                                          # optimize spacing
plt.savefig("images/top5_banks_market_cap.svg", dpi=300, bbox_inches='tight')

#  Display the chart
plt.show()



