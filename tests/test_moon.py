import pytest
import datetime
from flask import g, session
from moon_demo.db import get_db

def test_moon_page(client, app):
    date = datetime.datetime.now().strftime('%A %B %-d, %Y')
    response = client.get('/moon-phase')
    assert response.status_code == 200
    assert bytes(date, encoding='utf-8') in response.data
    assert b'illuminated' in response.data
    assert b'Full Moon' in response.data
    assert b'New Moon' in response.data
    assert b'First Quarter' in response.data
    assert b'Last Quarter' in response.data
    assert b'Image from NASA\'s Scientific Visualization Studio' in response.data

def test_moon_other_pages(client, app):
    response = client.get('/moon-phase/2019-03-13')
    assert b'Wednesday March 13, 2019' in response.data
    assert b'First Quarter' in response.data
    assert b'8 days until the next Full Moon' in response.data
    assert b'23 days until the next New Moon' in response.data
    assert b'1 days until the next First Quarter' in response.data
    assert b'16 days until the next Last Quarter' in response.data