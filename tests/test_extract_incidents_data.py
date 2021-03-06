import project0.project0 as project0

def test_extractincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
    data = project0.getincidentsdata(url)
    cleaneddata = project0.extractincidentsdata(data)
    assert cleaneddata[0] == '2/2/2022 0:03'

def test_extractwrongincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf"
    data = project0.getincidentsdata(url)
    cleaneddata = project0.extractincidentsdata(data)
    assert cleaneddata[0] != '1/2/2022 0:03'