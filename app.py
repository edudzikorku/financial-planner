# imports 
import os
import json
import psycopg2
from psycopg2 import  sql
import matplotlib.pyplot as plt
from datetime import datetime as dt

# initialize empty dictionary to store financial data
financial_data = {}


# create function to calculate the total income for the month
def total_income_per_month(year, month):
    if year in financial_data and month in financial_data[year]:
        return financial_data[year][month]['income']
    else:
        return 0

# create function to create bar chart showing income sources per month
def generate_income_source_chart(year, month):
    print(f"Generating chart for {month}, {year}")
    if year in financial_data and month in financial_data[year]:
        sources = [entry['source'] for entry in financial_data[year].values()]
        income_sources = {}
        for source in sources:
            if source in income_sources:
                income_sources[source] += 1
            else:
                income_sources[source] = 1
        # create bar chart
        plt.bar(income_sources.keys(), income_sources.values())
        plt.xlabel("Income  Source")
        plt.ylabel("Frequency")
        plt.title(f"Income Sources for {month}, '{year}")
        plt.xticks(rotation = 45)
        plt.show()
    else:
        print("Data not available for the specified month")

# set output directory
dir = "data/financial_data.json"


# creat function to save financial data to json file
def save_data():
    with open(dir, 'w') as file:
        json.dump({}, file)


user = 'postgres'
database = 'finance'
password = '0071005032'
schema = 'finance_planner'
table = 'finance_data'

try:
    # establish connection with database
    conn = psycopg2.connect(dbname = database, user = user, password = password)
    # create cursor object to execute queries
    with conn.cursor() as cursor:
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                        id SERIAL PRIMARY KEY,
                        year INTEGER,
                        month VARCHAR(255),
                        income (GH₵) NUMERIC,
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

    except psycopg2.Error as e:
        print("Error inserting data: ", e)


# create function to input income data for the current month and year
def create_income():
    income = float(input('Enter the income amount: '))
    source = input('Enter source: ')

    # save data to json file
    save_data()

    # save data to database
    save_data_to_db(income, source)
    print("Income data saved sussesfully.")

# main loop to provide income details
while True:
    print("\n Financial Planner Menu:")
    print("1. Enter Income Data for the Current Month")
    print("2. Calculate Monthly Total Income")
    print("3. Generate Income Source Chart")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        create_income()
    elif choice == '2':
        now = dt.now()
        year = now.strftime('%Y')
        month = now.strftime('%d-%m')
        total = total_income_per_month(year, month)
        print(f"Total income for {month}, {year}: $total; .2f")
    elif choice == '3':
        now = dt.now()
        year = now.strftime('%Y')
        month = now.strftime('%d-%m')
        generate_income_source_chart(year, month)
    elif choice == '4':
        save_data()
        break
    else:
        print("Invalid choice. Please try again")
