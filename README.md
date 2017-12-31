# LogAnalysisProject

This repository contains code that will connect to the "news" psql database and run queries on it to generate below reports:
1. Find the most popular three articles of all time
2. Find the most popular article authors of all time.
3. Find days on which more than 1% of requests lead to errors.

## Table of content
- [Requirements](#requirements)
- [Program Design](#program-design)
- [Running the code](#running-the-code)
- [Stopping the code](#stopping-the-code)

## Requirements
The following should be available on the machine/vm where the code is run:
- Postgresql with "news" database
- Python 2.7
- psycopg2 python library
- "SuccessfulllyReadArticlesView" view inside the "news" database. Sql to create the view is as follows:

CREATE VIEW SuccessfulllyReadArticlesView
(slug, method, status, id)
 AS
(
    SELECT
        SPLIT_PART(path, '/', 3) AS slug,
        method,
        status,
        id
    FROM log
    WHERE
    path LIKE '%article%' AND
    method = 'GET' AND
    status = '200 OK'
);

## Program Design
- The program ReportingTool.py contains three functions
- Each function generates one of the required reports
- Each function connects to the "news" psql database individually
- Then it runs required query for the report on the database
- The output is then printed out in the console in the required format
- The functions are called at the bottom of the script

## Running the code
- Connect to the psql "news" database
- Create the "SuccessfulllyReadArticlesView" view using the sql provide above
- Disconect from the psql database
- Pull the code from this repository to your local machine
- Navigate to the folder LogAnalysisProject
- Run the python code ReportingTool.py from the command prompt (if using Windows) or from the Terminal (if using Mac) using the command "python ReportingTool.py"
- The program will print reports output on the console as provided in the Output.txt file under LogAnalysisProject folder

## Stopping the code
- Close all command prompt/terminal windows that were opened