========================
README.md
========================
# Mini SQL Database (In-Memory)

##  Project Overview
This project is a simplified, in-memory SQL query engine built using Python.
It loads data from CSV files and allows users to execute basic SQL queries
such as SELECT, WHERE, and COUNT through a command-line interface.

The purpose of this project is to understand how SQL queries are parsed
and executed internally without using a real database.

---

##  Features
- Load CSV data into memory
- Store data as a list of dictionaries (one dictionary per row)
- Parse a subset of SQL queries
- Execute SELECT, WHERE, and COUNT queries
- Interactive command-line interface (REPL)
- Graceful error handling

---

##  Project Structure
Mini-SQL-database/
│
├── engine.py        # CSV loader and query execution engine
├── parser.py        # SQL parser
├── cli.py           # Command-line interface (REPL)
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    ├── employees.csv
    ├── users.csv
    └── products.csv

---

##  Setup and Usage

### Prerequisites
- Python 3.8 or higher
- No external libraries required (only Python standard library)

### Run the Application
python cli.py

When prompted, enter the CSV file path, for example:
data/employees.csv

---

##  Supported SQL Grammar

This engine supports a limited subset of SQL.

Supported Queries:
SELECT * FROM table_name;
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name WHERE column > value;
SELECT COUNT(*) FROM table_name;
SELECT COUNT(column_name) FROM table_name WHERE column = value;

Supported WHERE Operators:
=  !=  >  <  >=  <=

Not Supported:
- JOIN
- GROUP BY
- ORDER BY
- Multiple WHERE conditions
- INSERT, UPDATE, DELETE

---

##  Sample Datasets

The project includes multiple CSV files used for testing:

- employees.csv  
  Kaggle-derived employee dataset (15 rows)

- users.csv  
  Simple user dataset for validating SELECT and WHERE queries

- products.csv  
  Sample product dataset for testing SELECT and COUNT operations

---

## Error Handling
- Invalid SQL syntax produces a clear error message
- Querying non-existent columns raises informative errors
- Unsupported operations are handled gracefully

---

##  License
This project is for educational purposes only.


========================
.gitignore
========================
__pycache__/
*.pyc
*.pyo
.env
.DS_Store


========================
requirements.txt
========================
# No external dependencies required
# Uses only Python standard library
