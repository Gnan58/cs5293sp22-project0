# Gnaneswar Kolla


## Installation/Getting Started
---
1. Pipenv to create and manage virtual environment for the project.     
    > pipenv install
2. [Packages](#packages) required to run this project can be installed using below commands.
    > PyPDF2==1.26.0

    > pytest==7.0.1
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
    - Created a temporary file using `tempfile` module and write the bytes object data into that file.
        - tempfile module is used to create temporary files and directories.
    - Then `PyPDF2` package is used to perform operations on temporary file.
        - pdfReader object is used to get each page and extract text using extractText() method and splitting it with new line character to return each page data into a list.
        - Then if the page number is 1, it calls cleanfirstpage() method to clean data in first page and rest of the pages goes into  cleanotherpages() method and last page to cleanlastpage() method.
        - Once all pages data is appended to one list , the execution calls clean() method to handle all the edge cases in each row of a file and returns list of rows to insert data into database. 
3. `cleanfirstpage(page)` This function takes a page i.e a list of strings which is each element present in a first page and returns after cleaning the page data.
    - Cleaning here refers to taking only data from rows and excluding any headings, column names and whitespace character found in a page.
    - The column names are excluded from the list by finding the index of first element of first row with pattern matching.(DD/MM/YYYY HH:MM / D/M/YYYY HH:MM)
    - The headings of the report and white space character are excluded by slicing the list until last three items(pattern in first page). 
4. `cleanotherpages(page)` This function takes a page i.e list of string which is each element present in a page  and returns after cleaning the page data.
    - Cleaning here refers to removing white space character present in a list by slicing until last item.    
5. `cleanlastpage(page)` This function takes a page i.e list of string which is each element present in a page  and returns after cleaning the page data.
    - Cleaning here refers to removing white space character and date of report present in a list by slicing until last two item. 
3. `incidentORIcheck(st)` This function takes a partitionList of 5 elements and searches a regular expression pattern and return index of that string in a list.
    - Index if present in a list.
    - **O** if not present
6. `clean(rowsList)` This function takes rowslist and handles all the edge cases in a file.
    - First the rowsList is divided into 5 items into `partitionList`.
    - Then it checks for **Incident ORI** value using `incidentORICheck(st)` in that sublist and returns index `searchIndex` of that matched string.
        - If  `searchIndex` value is 4 then Incident ORI value is at last position of row and all the elements in that row are present and then that sublist is appended to `finalList`.
        - If `searchIndex` value is 3 then 
        first three elements of a row are present and since value of fourth element is missing it inserts **Unknown** value in that sublist and pushes the item in fourth index to last and then sublist is appended to `finalList`.
        - If `searchIndex` value is 2 then first two elements of a row are present and since values of third and fourth element is missing it inserts two **Unknown** values in that sublist and pushes item in third index to last and then sublist is appended to `finalList`.
        - If `searchIndex` value is 0 then location column in PDF file is split into two strings so it appends items at index 2 and 3 and inserts the appended value at index 2 and next elements to that temporary list and finally adding that to `finalList`.
    - `pointer` variable is used to keep track of the index of rowsList and finally each row in any given page will have five elements.


##  Approach to Developing the Database
---
1. `createdb()` This function creates an SQLite database file named **normanpd.db** and inserts the table **incidents** if not present and returns the connection object.
    - cursor() is an instance through which one can invoke methods that execute sqlite statements.
2. `populatedb(con, incidents)` This function takes incidents list from extractincidetsdata() method and divides 5 items from list and inserts that data to table created in createdb() method. 
3. `status(con)` This function prints nature of incidents and number of times it occur from incident table sorted by total no of incidents and alphabetically by the nature.
## Tests
---
1. **`test_get_incidents_data.py`**
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `getincidentsdata(url)`    |    `test_correctincidentsdata()`    |    when correct URL is passed ,it tests whether the recieved data is of type bytes.
    |   `getincidentsdata(url)`    |    `test_wrongincidentsdata()`    |    when wrong URL is passed, the execution terminates and prints message to give appropriate URL.
2. **`test_extract_incidents_data.py`**
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `extractincidentsdata(data)`    |    `test_extractincidents()`    |    Tests whether the extractsIncidents method extracts data correctly by asserting first value of list. 
    |   `extractincidentsdata(data)`    |    `test_extractwrongincidents()`    |    Tests whether the extractsIncidents method extracts data incorrectly by false asserting first value of list.

3. **`test_clean_first_page.py`**
    
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `cleanfirstpage(page)`    |    `test_cleanfirstpage()`    |    When a list with headings, column names and whitespace character are passed, it tests whether the data is cleaned by asserting first and last value of a list.
    |   `cleanfirstpage(page)`    |    `test_uncleanfirstpage()`    |    When a list with headings, column names and whitespace character are passed, it tests whether the data is not cleaned by false asserting first and last value of a list.

4. **`test_clean_other_pages.py`**
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `cleanotherpages(page)`    |    `test_cleanotherpages()`    |    Tests whether the last item is removed by asserting first and last value of a list.
    |   `cleanotherpages(page)`    |    `test_uncleanotherpages()`    |    Tests whether the last item is not removed by false asserting last value of a list.

5. **`test_clean_last_page.py`**
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `cleanlastpage(page)`    |    `test_cleanlastpage()`    |    Tests whether the last two items is removed by asserting first and last value of a list.
    |   `cleanlastpage(page)`    |    `test_uncleanlastpage()`    |    Tests whether the last two items is not removed by false asserting last value of a list.

3. **`test_incidentORI_check.py`**
    | Function | Test Function |    Parameter   | Description  |   
    |   --- |   --- |   --- |   ---
    |   `incidentORIcheck(st)`    |    `test_incidentORICheck(incidentORI, index)`    |   Parameter1  |    Tests when the pattern is found at index 4 .
    |   `incidentORIcheck(st)`    |    `test_incidentORICheck(incidentORI, index)`    |   Parameter2  |    Tests when the pattern is found at index 3.
    |   `incidentORIcheck(st)`    |    `test_incidentORICheck(incidentORI, index)`    |   Parameter3  |    Tests when the pattern is found at index 2.
    |   `incidentORIcheck(st)`    |    `test_incidentORICheck(incidentORI, index)`     |   Parameter4  |    Tests when the pattern is found at index 0.

6. **`test_clean.py`**
    | Function | Test Function |    Parameter   | Description  |   
    |   --- |   --- |   --- |   ---
    |   `clean(rowsList)`    |    `test_clean(rowList, cleanedList)`    |   Parameter1  |    Tests when the searchIndex is 4 and returns same list.
    |   `clean(rowsList)`    |    `test_clean(rowList, cleanedList)`    |   Parameter2  |    Tests when the searchIndex is 3 and inserts one **Unknown** value.
    |   `clean(rowsList)`    |    `test_clean(rowList, cleanedList)`    |   Parameter3  |    Tests when the searchIndex is 2 and inserts two **Unknown** value
    |   `clean(rowsList)`    |    `test_clean(rowList, cleanedList)`     |   Parameter4  |    Tests when the searchIndex is 0 and then concatenates index value of 2 and 3 and returns list.
7. **`test_createdb.py`**
    | Function | Test Function |    Parameter   | Description  |   
    |   --- |   --- |   --- |   ---
    |   `createdb()`    |    `test_createdb(setup_database)`    |   Parameter is a fixture  |    Tests whether the return value of method is of type connection from fixture.
8. **`populatedb.py`**
    | Function | Test Function |    Parameter   | Description  |   
    |   --- |   --- |   --- |   ---
    |   `populatedb(con, incidents)`    |    `test_populatedb(setup_test_data)`    |   Parameter is a fixture to setup test data  |    Tests whether the return value of no of rows inserted when given sample data asserts to expected value.
9. **`test_status.py`**
    | Function | Test Function |    Parameter   | Description  |   
    |   --- |   --- |   --- |   ---
    |   `status(con)`    |    `test_status(setup_database, capfd)`    |   Parameter1 is a fixture to setup test data. Parameter2 allows access to stdout/stderr output created   |    Tests whether the return value of no of rows inserted when given sample data asserts to expected value.