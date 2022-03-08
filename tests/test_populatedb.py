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
    yield con
    con.close()

@pytest.fixture
def setup_test_data(setup_database):
    cur = setup_database
    incidents = ['2/6/2022 23:17', '2022-00001877', '17901 E STATE HWY 9 HWY', 'Breathing Problems', '14005', '2/6/2022 23:22', '2022-00006619', 'Unknown Nature', 'Unknown Nature', '14009']
    yield cur, incidents

def test_populatedb(setup_test_data):
    cur, incidents = setup_test_data
    project0.populatedb(cur, incidents)
    rows = cur.execute('select * from incidents')
    assert len(rows.fetchall()) == 2
