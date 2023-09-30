## Financial Planner

### Overview
The Financial Planner is a Python-based program designed to facilitate effective management of personal finances. It provides a simple and user-friendly interface to input income data, calculate total monthly income, and export data for further analysis. The program utilizes a PostgreSQL database for robust data storage and retrieval and includes a JSON file for additional data persistence.

### Features
* Income Data Entry: <br />
Users can easily enter income data for the current month, specifying the amount and the source of income.

* Total Monthly Income Calculation: <br />
The program calculates and presents the total income for the current month, providing valuable insights for financial planning.

* CSV Data Export: <br />
You have the option to export financial data to a CSV file, allowing for external analysis and reporting.

* Error Handling: <br />
Robust error-handling mechanisms have been implemented to ensure program stability, providing meaningful feedback in case of unexpected issues.

* Multi-Platform Integration: <br />
The program seamlessly integrates with both a PostgreSQL database and a JSON file, ensuring comprehensive data storage and accessibility.

### Usage
#### Clone the Repository:

```
git clone https://github.com/your-username/financial-planner.git 

cd financial-planner
```


#### Install Dependencies: 
``` 
pip install -r requirements.txt 
```
#### Set Up PostgreSQL Database:

- Create a PostgreSQL database and schema for the Financial Planner. Update the user, password, database, and schema variables in the app.py file with your database details.

#### Run the Program:

#### Interact with the Menu:
- Follow the on-screen menu to enter income data, calculate total monthly income, export data, or exit the program.

#### Example Interaction 
```
Financial Planner Menu:
1. Enter Income Data for the Current Month
2. Calculate Monthly Total Income
3. Save data to CSV
4. Exit

Enter your choice (1/2/3/4): 1

Enter the income amount: 500.00
Enter source: Gift

Income data saved successfully.
```