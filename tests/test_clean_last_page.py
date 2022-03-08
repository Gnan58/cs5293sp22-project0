import project0.project0 as project0

def test_cleanlastpage():
    page = ['2/6/2022 23:22', '2022-00006619', '1544 OK-9', 'Assist Fire', 'OK0140200', '2/6/2022 23:24', '2022-00006618', '444 W ROBINSON ST', 'Traffic Stop', 'OK0140200', '2/7/2022 10:25', '']
    expected = project0.cleanlastpage(page)
    assert expected[0] == '2/6/2022 23:22'
    assert expected[-1] == 'OK0140200'

def test_uncleanlastpage():
    page = ['2/6/2022 23:22', '2022-00006619', '1544 OK-9', 'Assist Fire', 'OK0140200', '2/6/2022 23:24', '2022-00006618', '444 W ROBINSON ST', 'Traffic Stop', 'OK0140200', '2/7/2022 10:25', '']
    expected = project0.cleanlastpage(page)
    assert expected[0] == '2/6/2022 23:22'
    assert expected[-1] != ' '