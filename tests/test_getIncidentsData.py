import project0.project0 as project0

def test_getIncidentsData():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
    data = project0.getIncidentsData(url)
    assert isinstance(data, bytes)