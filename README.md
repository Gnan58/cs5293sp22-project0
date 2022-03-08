# Gnaneswar Kolla

## Installation/Getting Started
---
1. Pipenv to create and manage virtual environment for the project.     
    > pipenv install
2. [Packages](#packages) required to run this project can be installed using below commands.
    > pipenv install PyPDF2

    > pipenv install pytest
3. Once, the packages are successfully installed, the project can be executed using 
    > pipenv run python project0/main.py --incidents URL

    **URL** must only be a daily incident summary report from [Norman Police Department Activity](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports) for this project.

## Packages
---
- `PyPDF2` is a python library used to perform various tasks on a PDF file. 
    - In this project, PyPDF2 is used to extract data from a PDF file.
    - [PyPDF2.pdf.PdfFileReader](https://pythonhosted.org/PyPDF2/PdfFileReader.html) class is used to create a pdf reader object and extract data from a file
- `pytest` is a framework to write small, readable tests, and can scale to support complex functional testing for applications and libraries.
    - In this project, pytest is used to create [unit tests](#tests) for each functionality
## Assumptions
---
1. Assuming URL of Incident Summary report has word **incident** in it. 
2. Assuming last column i.e **Incident ORI** in PDF has only 3 patterns/kind of values.
    - OK0140200
    - EMSSTAT
    - First four digits of value as 1400
3. Assuming columns 1,2 and 5 in PDF are **always** present in any given row.
4. Assuming column 3 i.e Location is split into maximum of **2** lines in any given row.
##  Approach to Developing the code
---
1. `getincidentsdata(url)` 
    This function takes url string as a parameter, checks and grabs an incident PDF document from the website URL and returns data in bytes.
    - `urllib.request` library is used to open the url and read data.
        - Extensible library for opening URLs 

2. `extractincidentsdata(data)` This function takes data from a PDF file, extracts incidents and handles all the edge cases encountered in each row to return a list of rows.
    - th
3. `cleanfirstpage(page)` This function takes a page i.e a list of strings which is each element present in a first page and returns after cleaning the page data.
    - Cleaning here refers to taking only data from rows and excluding any headings, column names and whitespace character found in a page.
    - The column names are excluded from the list by finding the index of first element of first row with pattern matching.(DD/MM/YYYY HH:MM / D/M/YYYY HH:MM)
    > ^([1-9]|([012][0-9])|(3[01]))/([0]{0,1}[1-9]|1[012])/\d\d\d\d [012]{0,1}[0-9]:[0-6][0-9]$
    - The headings of the report and white space character are excluded by slicing the list until last three items(pattern in first page). 
4. `cleanotherpages(page)` This function takes a page i.e list of string which is each element present in a page  and returns after cleaning the page data.
    - Cleaning here refers to removing white space character present in a list by slicing until last item.    
5. `cleanlastpage(page)` This function takes a page i.e list of string which is each element present in a page  and returns after cleaning the page data.
    - Cleaning here refers to removing white space character and date of report present in a list by slicing until last two item.    

## Tests
---
1. `test_get_incidents_data.py`
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `getincidentsdata(url)`    |    `test_correctincidentsdata()`    |    when correct URL is passed ,it tests whether the recieved data is of type bytes.
    |   `getincidentsdata(url)`    |    `test_wrongincidentsdata()`    |    when wrong URL is passed, the execution terminates and prints message to give appropriate URL.
2. 
3. `test_clean_first_page.py`
    
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `cleanfirstpage(page)`    |    `test_cleanfirstpage()`    |    When a list with headings, column names and whitespace character are passed, it tests whether the data is cleaned by asserting first and last value of a list.
    |   `cleanfirstpage(page)`    |    `test_uncleanfirstpage()`    |    When a list with headings, column names and whitespace character are passed, it tests whether the data is not cleaned by false asserting first and last value of a list.
4. `test_clean_other_pages.py`
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `cleanotherpages(page)`    |    `test_cleanotherpages()`    |    Tests whether the last item is removed by asserting first and last value of a list.
    |   `cleanotherpages(page)`    |    `test_uncleanotherpages()`    |    Tests whether the last item is not removed by false asserting last value of a list.
5. `test_clean_last_page.py`
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `cleanlastpage(page)`    |    `test_cleanlastpage()`    |    Tests whether the last two items is removed by asserting first and last value of a list.
    |   `cleanlastpage(page)`    |    `test_uncleanlastpage()`    |    Tests whether the last two items is not removed by false asserting last value of a list.