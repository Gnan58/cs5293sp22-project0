import project0.project0 as project0

def test_cleanOtherPages():
    page = ['2/6/2022 1:16', '2022-00006506', '1612 OAKCREST AVE', 'Medical Call Pd Requested', 'OK0140200', '2/6/2022 1:22', '2022-00006507', '304 PINE COVE CT', 'Welfare Check', 'OK0140200', ' ']
    expected = project0.cleanOtherPages(page)
    assert expected[0] == '2/6/2022 1:16'
    assert expected[-1] == 'OK0140200'

def test_uncleanOtherPages():
    page = ['2/6/2022 1:16', '2022-00006506', '1612 OAKCREST AVE', 'Medical Call Pd Requested', 'OK0140200', '2/6/2022 1:22', '2022-00006507', '304 PINE COVE CT', 'Welfare Check', 'OK0140200', ' ']
    expected = project0.cleanOtherPages(page)
    assert expected[0] == '2/6/2022 1:16'
    assert expected[-1] != ' '