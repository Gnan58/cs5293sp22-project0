import project0.project0 as project0

def test_correctincidentsdata():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
    data = project0.getincidentsdata(url)
    assert isinstance(data, bytes)

def test_wrongincidentsdata(capfd):
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_arrests_summary.pdf"
    project0.getincidentsdata(url)
    out, err = capfd.readouterr()
    assert out == 'Wrong URL! Please provide Incident Summary URL\n'
