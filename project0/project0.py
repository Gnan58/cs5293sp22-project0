import urllib.request
import tempfile
import PyPDF2
import re
import sqlite3


def getincidentsdata(url):
    '''
    To open the URL url, and read data.

    Parameter
    ----------
    url : str
        A string which contains the URL of incident summary report.

    Returns
    -------
        Data from a PDF file in bytes
    '''
    if (re.search(r'incident', url)):
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        return data
    else:
        print('Wrong URL! Please provide Incident Summary URL')


def extractincidentsdata(data):
    '''
    Extracts each row from a PDF file and handles all the edge cases in a file.

    Parameter
    ---------
    data : bytes
        Data in bytes from a PDF file

    Return
    ------
        Each element in a row as a string in list
    '''
    rowsList = []
    fp = tempfile.TemporaryFile()
    fp.write(data)
    fp.seek(0)
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pagecount = pdfReader.getNumPages()
    for pageNumber in range(0, pagecount):
        page = pdfReader.getPage(pageNumber).extractText().split("\n")
        if pageNumber == 0:
            page = cleanfirstpage(page)
        elif pageNumber == pagecount - 1:
            page = cleanlastpage(page)
        else:
            page = cleanotherpages(page)
        for data in page:
            rowsList.append(data)
    cleanedData = clean(rowsList)
    return cleanedData


def incidentORIcheck(st):
    """
    Search a regular expression pattern with in a string

    Parameter
    ---------
    st : list
        A partition list to find index of Location ORI
    Returns
    -------
        Index of matched string in a list, o if not matched
    """
    index = [
        i
        for i, item in enumerate(st)
        if re.search(r"OK(\d{7})", item)
        or re.search(r"1400([0-9]{1})", item)
        or re.search(r"EMSSTAT", item)
    ]
    if index:
        return index[0]
    else:
        return 0


def cleanfirstpage(page):
    """
    Removes headings, column names and whitespace character present in first page of PDF.

    Parameters
    -----------
    page : list
        A list of Strings which is each element in a PDF page.

    Returns
    -------
        List without headings, column names and whitespace characters.
    """
    ide = [
        i
        for i, item in enumerate(page)
        if re.search(
            r"^([1-9]|([012][0-9])|(3[01]))/([0]{0,1}[1-9]|1[012])/\d\d\d\d [012]{0,1}[0-9]:[0-6][0-9]$",
            item,
        )
    ]
    return page[ide[0] : -3]


def cleanotherpages(page):
    """
    Removes last item in a list

    Parameters
    -----------
    page : list
        A list of Strings which is each element in a PDF page.

    Returns
    -------
        A List
    """
    return page[0:-1]


def cleanlastpage(page):
    """
    Removes last two items in a list

    Parameters
    -----------
    page : list
        A list of Strings which is each element in a PDF page.

    Returns
    -------
        A List
    """
    return page[0:-2]


def clean(rowsList):
    """
    Handles edge cases of each row in a PDF file

    When column 4 i.e Nature value in PDF is not present,this function inserts "Unknown Nature" value for that column.

    When column 3 i.e Location value is split into multiple blocks, this function appends them.

    Parameter
    ---------
    rowsList : list
        A list of strings which is each element from all pages in a PDF file.

    Returns
    -------
        A list with all rows in a PDF file.
    """
    partitionList = []
    finalList = []
    pointer = 0
    count = 0
    while pointer < len(rowsList):
        if count < 5:
            partitionList.append(rowsList[pointer])
            count += 1
            pointer += 1
        searchIndex = incidentORIcheck(partitionList)
        if count == 5 and searchIndex == 0:
            tempList = []
            for i in range(0, 2):
                tempList.append(partitionList[i])
            address = partitionList[2] + " " + partitionList[3]
            tempList.insert(2, address)
            tempList.insert(3, partitionList[-1])
            tempList.insert(4, rowsList[pointer])
            pointer += 1
            partitionList = tempList
        if count == 5 or pointer == len(rowsList):
            searchIndex = incidentORIcheck(partitionList)
            if searchIndex == 4:
                for i in range(0, searchIndex + 1):
                    finalList.append(partitionList[i])
                count = 0
                partitionList = []
            elif searchIndex == 3:
                for i in range(0, searchIndex):
                    finalList.append(partitionList[i])
                noUnknownValues = 4 - searchIndex
                for times in range(0, noUnknownValues):
                    finalList.append("Unknown")
                finalList.append(partitionList[searchIndex])
                pointer -= noUnknownValues
                count = 0
                partitionList = []
            elif searchIndex == 2:
                for i in range(0, searchIndex):
                    finalList.append(partitionList[i])
                noUnknownValues = 4 - searchIndex
                for times in range(0, noUnknownValues):
                    finalList.append("Unknown")
                finalList.append(partitionList[searchIndex])
                pointer -= noUnknownValues
                count = 0
                partitionList = []
    return finalList


def createdb():
    """
    Creates an SQLite database file and inserts table .

    Returns
    -------
        connection object
    """
    con = sqlite3.connect("normanpd.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS incidents")
    cur.execute(
        """CREATE TABLE incidents
            (incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT)"""
    )
    con.commit()
    return con


def populatedb(con, incidents):
    """
        Inserts incidents data into database

    Parameter
    ---------
    con : connection object
    incidents : list
        list of incident rows from PDF file
    """
    cur = con.cursor()
    lst_tuple = [x for x in zip(*[iter(incidents)] * 5)]
    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", lst_tuple)
    con.commit()


def status(con):
    """
        prints the nature of incidents and no of times it occur from incidents table

    Parameter
    ----------
    con : connection object

    """
    cur = con.cursor()
    rows = cur.execute(
        "SELECT nature, count(*)  FROM incidents group by nature order by count(*) DESC , nature ASC"
    ).fetchall()
    for i in rows:
        print(i[0], "|", i[1])
    con.close()
