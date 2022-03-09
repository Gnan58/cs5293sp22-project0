import sqlite3

import pytest

import project0.project0 as project0

@pytest.fixture
def setup_database():
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS incidents")
    cur.execute("""CREATE TABLE incidents
            (incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT)""")
    incidents = ['2/6/2022 23:17', '2022-00001877', '17901 E STATE HWY 9 HWY', 'Breathing Problems', '14005', '2/6/2022 23:17', '2022-00002403', '17901 E STATE HWY 9 HWY', 'Breathing Problems', 'EMSSTAT', '2/6/2022 23:18', '2022-00006620', '1357 12TH AVE NE', 'Contact a Subject', 'OK0140200']
    lst_tuple = [x for x in zip(*[iter(incidents)] * 5)]
    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", lst_tuple)
    yield con
    con.close()

def test_status(setup_database, capfd):
    con= setup_database
    project0.status(con)
    out, err = capfd.readouterr()
    assert out == 'Breathing Problems | 2\nContact a Subject | 1\n'