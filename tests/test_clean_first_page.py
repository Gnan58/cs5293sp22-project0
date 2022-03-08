import project0.project0 as project0

def test_cleanFirstPage():
    page = ['Date / Time', 'Incident Number', 'Location', 'Nature', 'Incident ORI', '2/6/2022 0:01', '2022-00006502 60TH AVE NE / E FRANKLIN RD', 'Motorist Assist', 'OK0140200', 'NORMAN POLICE DEPARTMENT', 'Daily Incident Summary (Public)', ' ']
    expected = project0.cleanFirstPage(page)
    assert expected[0] == '2/6/2022 0:01'
    assert expected[-1] == 'OK0140200'

def test_uncleanFirstPage():
    page = ['Date / Time', 'Incident Number', 'Location', 'Nature', 'Incident ORI', '2/6/2022 0:01', '2022-00006502 60TH AVE NE / E FRANKLIN RD', 'Motorist Assist', 'OK0140200', 'NORMAN POLICE DEPARTMENT', 'Daily Incident Summary (Public)', ' ']
    expected = project0.cleanFirstPage(page)
    assert expected[0] != 'Date / Time'
    assert expected[-1] != ' '