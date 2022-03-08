import project0.project0 as project0
import pytest

@pytest.mark.parametrize("rowList, cleanedList", [(['2/6/2022 0:22', '2022-00002355', '3737 W MAIN ST', 'Assault EMS Needed', 'EMSSTAT'], ['2/6/2022 0:22', '2022-00002355', '3737 W MAIN ST', 'Assault EMS Needed', 'EMSSTAT']),
                                                (['2/6/2022 23:22', '2022-00006619', '1544 OK-9', 'OK0140200', 'Assist Fire'], ['2/6/2022 23:22', '2022-00006619', '1544 OK-9', 'Unknown', 'OK0140200']),
                                                (['2/6/2022 23:22', '2022-00006619', '14009', '0140200', 'Assist Fire'], ['2/6/2022 23:22', '2022-00006619', 'Unknown', 'Unknown', '14009']),
                                                (['2/6/2022 23:22', '2022-00006619', 'N FLOOD AVE/I35 SB OFF RAMP 113', 'RAMP', 'Assist Fire', 'OK0140200'], ['2/6/2022 23:22', '2022-00006619', 'N FLOOD AVE/I35 SB OFF RAMP 113 RAMP', 'Assist Fire', 'OK0140200'])])

def test_clean(rowList, cleanedList):
    assert project0.clean(rowList) == cleanedList