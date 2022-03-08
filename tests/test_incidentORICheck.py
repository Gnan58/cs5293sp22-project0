import project0.project0 as project0
import pytest

@pytest.mark.parametrize("incidentORI, index", [(['2/6/2022 0:22', '2022-00002355', '3737 W MAIN ST', 'Assault EMS Needed', 'EMSSTAT'], 4),
                                                (['2/6/2022 23:22', '2022-00006619', '1544 OK-9', 'OK0140200', 'Assist Fire'], 3),
                                                (['2/6/2022 23:22', '2022-00006619', '14009', '0140200', 'Assist Fire'], 2),
                                                (['2/6/2022 23:22', '2022-00006619', '1544 OK-9', 'Assist Fire', '0140200'], 0)])

def test_incidentORICheck(incidentORI, index):
    assert project0.incidentORICheck(incidentORI) == index