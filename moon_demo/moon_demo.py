from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from moon_demo.auth import login_required
from moon_demo.db import get_db

import datetime
import dateparser
import inflect

from . import moonpy

bp = Blueprint('moon_page', __name__)

@bp.route('/moon-phase')
def moon_page():
    phase_data = get_phase_data()
    return render_template('moon_phases/index.html', phase_data=phase_data)

@bp.route('/moon-phase/<date>')
def other_moon(date):
    parsed_date = _validate_date(date)
    if not parsed_date:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    phase_data = get_phase_data(date)
    return render_template('moon_phases/index.html', phase_data=phase_data)

def get_phase_data(date=None):
    phase_data = {}
    moon = moonpy.MoonPy(date)
    phase_date = moon.phase_date
    prevnext = get_prev_next(phase_date)
    phase_data = {
        'name': moon.get_phase_name(),
        'date': phase_date,
        'id': str(moon.get_image()).zfill(2),
        'illum': moon.get_percentage_of_illumination(),
        'prev': prevnext['prev'].strftime("%Y-%m-%d"),
        'next': prevnext['next'].strftime("%Y-%m-%d"),
    }
    milestones = [
        'new moon',
        'first quarter',
        'full moon',
        'last quarter'
    ]
    p = inflect.engine()
    for val in milestones:
        days = moon.get_days_until_next_moon(val)
        plural = p.plural('day', days)
        phase_data[val] = ('{} {} until next {}').format(days, plural, val)

    return phase_data

def get_prev_next(date):
    phase_date = datetime.datetime.fromtimestamp(date)
    prevnext = {
        'prev': phase_date - datetime.timedelta(1),
        'next': phase_date + datetime.timedelta(1),
    }
    return prevnext

def _validate_date(date):
    '''Check that the value provided for the date is able to be parsed.'''
    if isinstance(dateparser.parse(date), datetime.datetime):
        validatetime = True
    else:
        flash('"{}" is not a valid date format. Showing current moon phase instead.'.format(date), 'error')
        validatetime = False
    return validatetime

