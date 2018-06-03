# LogAnalysisProject

This project sets up a mock PostgreSQL database for a fictional news website. The provided Python script uses the psycopg2 library to query the database and produce reports that answer the following three questions:
1. Find the most popular three articles of all time
2. Find the most popular article authors of all time
3. Find days on which more than 1% of requests lead to errors

## Table of content
- [Requirements](#requirements)
- [Program Design](#program-design)
- [Setting up the mock database](#setting-up-the-mock-database)
- [Running the Python script](#running-the-python-script)
- [Stopping the Python script](#stopping-the-python-script)

## Requirements
The following should be available on the machine/vm where the code is run:
- PostgreSQL
- Python 2.7
- psycopg2 Python library

## Program Design
- The script [ReportingTool.py](https://github.com/dgpshiva/LogAnalysisProject/blob/master/ReportingTool.py) contains four functions
- 'execute_query' is a helper function that connects to the database, runs the provided query and returns the results of the query
- Each of the other functions generate one of the required reports
- Each function passes the required query to the 'execute_query' helper function and gets the results back
- The results output is then formatted and printed out in the console
- The functions are called at the bottom of the script


## Setting up the mock database
1. Create the "news" database in PostgreSQL
    - From the command line, launch the psql console by typing: ```psql```
    - Check to see if a news database already exists by listing all databases with the command: ```\l```
    - If a news database already exists, drop it with the command:
    ```sql
        DROP DATABASE news;
    ```
    - Create the news database with the command:
    ```sql
    CREATE DATABASE news;
    ```
    - Exit the console by typing: ```\q```

2. Download the schema and data for the news database:
    - [Click here to download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

3. Unzip the downloaded file ```unzip newsdata.zip```
    - You should now have an sql script called 'newsdata.sql'

4. From the command line, navigate to the directory containing 'newsdata.sql'

5. Import the schema and data in 'newsdata.sql' to the "news" database by typing: ```psql -d news -f newsdata.sql```



## Running the Python script
- Pull the code from this repository to your local machine
- Navigate to the folder '\LogAnalysisProject'
- Run the python code [ReportingTool.py](https://github.com/dgpshiva/LogAnalysisProject/blob/master/ReportingTool.py) from the command prompt (if using Windows) or from the Terminal (if using Mac) using the command ```python ReportingTool.py```
- The program will print reports output on the console as provided in the 'Output.txt' file under 'LogAnalysisProject' folder

## Stopping the Python script
- Close all command prompt/terminal windows that were opened
