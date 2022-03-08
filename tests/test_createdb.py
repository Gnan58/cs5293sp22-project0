import pytest
import sqlite3

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

def test_createdb(setup_database):
    con = setup_database
    assert isinstance(project0.createdb(), type(con))