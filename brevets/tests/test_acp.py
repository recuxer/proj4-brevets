"""
author: john nemeth
sources: heavy reference from class material
description: nose tests for acp_times.py
"""
from acp_times import open_time, close_time
import arrow
import nose

def test_over_brevet_distance_start():
    #test for result from giving control distance over brevet distance for start time
    assert not open_time(201, 200, arrow.utcnow())

def test_over_brevet_distance_close():
    #testing control over brevet distance for closetime
    assert not close_time(201, 200, arrow.utcnow())

def test_control_open():
    #testing opentime of a control by grabbing current time and shifting by known hour value
    begintime = arrow.utcnow()
    assert open_time(100, 400, begintime) == begintime.shift(hours=2.941).isoformat()
    assert open_time(200, 600, begintime) == begintime.shift(hours=5.882).isoformat()

def test_control_close():
    #testing closetime of control by getting current time and shifting by known hour value
    closetime = arrow.utcnow()
    assert close_time(100, 800, closetime) == closetime.shift(hours=6.667).isoformat()
    assert close_time(200, 1000, closetime) == closetime.shift(hours=13.333).isoformat()

def test_first_control():
    #to test first control point of zero
    closetime = arrow.utcnow()
    assert close_time(0, 1000, closetime) == closetime.shift(hours=1).isoformat()
