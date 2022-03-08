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
    tempFile = tempfile.TemporaryFile()
    tempFile.write(data)
    tempFile.seek(0)
    pdfReader = PyPDF2.pdf.PdfFileReader(tempFile)
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


def incidentORICheck(st):
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
    partitionList = []
    finalArray = []
    pointer = 0
    count = 0
    while pointer < len(rowsList):
        if count < 5:
            partitionList.append(rowsList[pointer])
            count += 1
            pointer += 1
        searchIndex = incidentORICheck(partitionList)
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
            searchIndex = incidentORICheck(partitionList)
            if searchIndex == 4:
                for i in range(0, searchIndex + 1):
                    finalArray.append(partitionList[i])
                count = 0
                partitionList = []
            elif searchIndex == 3:
                for i in range(0, searchIndex):
                    finalArray.append(partitionList[i])
                noUnknownValues = 4 - searchIndex
                for times in range(0, noUnknownValues):
                    finalArray.append("Unknown Nature")
                finalArray.append(partitionList[searchIndex])
                pointer -= noUnknownValues
                count = 0
                partitionList = []
            elif searchIndex == 2:
                for i in range(0, searchIndex):
                    finalArray.append(partitionList[i])
                noUnknownValues = 4 - searchIndex
                for times in range(0, noUnknownValues):
                    finalArray.append("Unknown Nature")
                finalArray.append(partitionList[searchIndex])
                pointer -= noUnknownValues
                count = 0
                partitionList = []
    return finalArray


def createdb():
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
    cur = con.cursor()
    lst_tuple = [x for x in zip(*[iter(incidents)] * 5)]
    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", lst_tuple)
    con.commit()


def status(con):
    cur = con.cursor()
    rows = cur.execute(
        "SELECT nature, count(*)  FROM incidents group by nature order by count(*) DESC , nature ASC"
    ).fetchall()
    for i in rows:
        print(i[0], "|", i[1])
    con.close()
