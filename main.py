######################################################################################
#                                                                                    #
# This is a simple program for recording income earned in every month                #
# It records the amount earned as well as the source of the income                   #
# The input from the user is then written to a PostgresSQL database                  #
#                                                                                    #
# Prepared by Edudzi (2023)                                                          #
######################################################################################

# imports 
import config
import os
import json
import psycopg2
import pandas as pd
from psycopg2 import  sql
from datetime import datetime as dt
from sqlalchemy import create_engine
from credentials import user, database, password, schema, table


# create sqlalchemy engine
engine = create_engine(f"postgresql://{user}:{password}@localhost:5432/{database}")
# set output directory
dir = config.OUTPUT_DIR

# create function to load existing data from json file
def load_json_file():  
    try:
        with open(dir, 'r') as json_file:       
            return json.load(json_file)
    except FileNotFoundError:
        return {"entries": []}
    
# create function to create or update json file with new entry
def update_json_file(entry):
    data = load_json_file()
    data["entries"].append(entry)
    with open(dir, 'w') as json_file:
        json.dump(data, json_file, indent = 2)


try:
    # establish connection with database
    conn = psycopg2.connect(dbname = database, user = user, password = password)
    # create cursor object to execute queries
    with conn.cursor() as cursor:
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                        id SERIAL PRIMARY KEY,
                        year INTEGER,
                        month VARCHAR(8),
                        income NUMERIC,
                        source VARCHAR(255)
);
"""
        # execute_query
        cursor.execute(create_table_query)
        # commit the changes
        conn.commit()
except psycopg2.Error as e:
    print("Error creating table: ", e)
    

#  create function to store financial data to database
def save_data_to_db(income, source):
    now = dt.now()
    year = now.strftime('%Y')
    month = now.strftime('%d-%m')
    month_ii = now.strftime('%m-%d')

    insert_query = sql.SQL(f"""
        INSERT INTO {schema}.{table} (year, month, income, source)
                   VALUES (%s, %s, %s, %s)
                   """)
    try:
        # establish connection with database
        conn = psycopg2.connect(dbname = database, user = user, password = password)
        # create cursor object to execute queries
        with conn.cursor() as cursor:
            # execute_query
            cursor.execute(insert_query, (year, month, income, source))
            # commit the changes
            conn.commit()
        entry = {"date": f"{month_ii}-{year}", "income": income, "source": source}
        update_json_file(entry)
    except psycopg2.Error as e:
        print("Error inserting data to database: ", e)
    except Exception as e:
        print("Error: ", e)
    finally:
        if conn:
            conn.close()


# create function to input income data for the current month and year
def create_income():
    income = None
    source = None
    while income is None:
        try:
            income = float(input('Enter the income amount: '))
        except ValueError:
            print("Invalid input. Please enter a valid income amount")
    while source is None:
        try:
            income_source = input(str('Enter source: '))
            if not all(character.isalpha() or character.isspace() for character in income_source):
                raise ValueError("Invalid input. Please enter a valid income source (eg. Salary, Freelance, Gift, e.t.c.)")
            source = income_source.title()
        except ValueError:
            print("Invalid income source. Please enter a valid income source (eg. Salary, Freelance, Gift, e.t.c.)")


    # save data to database
    save_data_to_db(income, source)
    print("Income data saved sussesfully.")

# create function to calculate the total income for the month
def total_income_per_month(year, month):
    # obtain full month name
    full_month_name = dt.strptime(month, '%d-%m').strftime('%B')
    query = (f"""
SELECT SUM(income) AS total_income 
                    FROM {schema}.{table}
                    WHERE year = %s AND month = %s
""")
    conn = psycopg2.connect(dbname = database, user = user, password = password)
    with conn.cursor() as cursor:
        cursor.execute(query, (year, month))
        total = cursor.fetchone()[0]
        if total is not None:
            return total, full_month_name
        else:
            return 0, full_month_name

# create function to retrieve data into pandas dataframe
def retrieve_data_as_dataframe(year, month):
    query = f"""
        SELECT *
        FROM {schema}.{table}
        WHERE year = %s AND month = %s
    """
    conn = engine.connect()
    df = pd.read_sql_query(query, conn, params = (year, month))
    return df

# create function to save data as csv

def save_file(df, filename):
    df.to_csv(filename, index = False)

# main loop to provide income details
while True:
    print("\n Financial Planner Menu:")
    print("1. Enter Income Data for the Current Month")
    print("2. Calculate Monthly Total Income")
    print("3. Save data to CSV")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        create_income()
    elif choice == '2':
        now = dt.now()
        year = now.strftime('%Y')
        month = now.strftime('%d-%m')
        total, full_month_name = total_income_per_month(year, month)
        print(f"Total income for {full_month_name}, {year}: GH₵{total:.2f}")

    elif choice == '3':
        now = dt.now()
        year = now.strftime('%Y')
        month = now.strftime('%d-%m')
        full_month = now.strptime(month, '%d-%m').strftime("%B")
        df = retrieve_data_as_dataframe(year, month)
        csv_filename = f"data/financial_data_{full_month}_{year}.csv"
        save_file(df, csv_filename)
        print(f"Data saved to {csv_filename}")

    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again")
