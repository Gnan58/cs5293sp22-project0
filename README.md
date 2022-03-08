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
1. Assuming last column i.e Incident ORI in PDF has only 3 patterns/kind of values.
    - OK0140200
    - EMSSTAT
    - First four digits of value as 1400
2. Assuming columns 1,2 and 5 in PDF are always present in any given row.
3. Assuming column 3 i.e Location is split into maximum of 2 lines in any given row.
##  Approach to Developing the code
---
1. `getIncidentsData(url)` 
    This function takes url string as a parameter and gets an incident PDF document from the website URL and returns data in bytes.
    - `urllib.request` library is used to open the url and read data.
        - Extensible library for opening URLs 
    -   Disabled default certificate verification using SSL module since 
    > ssl._create_default_https_context = ssl._create_unverified_context
2. ``
## Tests
---