"""
author: john nemeth
sources: heavy reference from class material
description: nose tests for acp_times.py
"""
from acp_times import open_time, close_time
import arrow
import nose

def test_control_open():
    #testing opentime of a control by grabbing current time and shifting by known equation
    begintime = arrow.utcnow()
    assert open_time(100, 400, begintime) == begintime.shift(hours=(100/34)).isoformat() 
    assert open_time(200, 600, begintime) == begintime.shift(hours=(200/34)).isoformat() 
    assert open_time(850, 1000, begintime) == begintime.shift(hours=(200/34 + 200/32 + 200/30 + 250/28)).isoformat()

def test_control_close():
    #testing closetime of control by getting current time and shifting by known equation
    closetime = arrow.utcnow()
    assert close_time(100, 800, closetime) == closetime.shift(hours=100/15).isoformat()
    assert close_time(500, 1000, closetime) == closetime.shift(hours=500/15).isoformat()
    assert close_time(625, 1000, closetime) == closetime.shift(hours=200/15 + 200/15 + 200/15 + 25/11.428).isoformat()

def test_first_control():
    #to test first control point of zero
    closetime = arrow.utcnow()
    assert close_time(0, 1000, closetime) == closetime.shift(hours=1).isoformat()

def test_200brev_endtime():
    #to test the endtime of 200km brevet
    closetime = arrow.utcnow()
    addedminutes = closetime.shift(minutes=10)
    assert close_time(200, 200, closetime) == addedminutes.shift(hours=200/15).isoformat()

def test_400brev_endtime():
    #to test endtime of 400km brevet
    closetime = arrow.utcnow()
    addedminutes = closetime.shift(minutes=20)
    assert close_time(400, 400, closetime) == addedminutes.shift(hours=400/15).isoformat()

def test_20perc_open():
    #for whether final control is within accepted 120% range of brevets for opentime 
    begintime = arrow.utcnow()
    assert open_time(240, 200, begintime) == begintime.shift(hours=200/34).isoformat()
    assert open_time(241, 200, begintime) == False
    assert open_time(360, 300, begintime) == begintime.shift(hours=200/34 + 100/32).isoformat()
    assert open_time(361, 300, begintime) == False
    assert open_time(480, 400, begintime) == begintime.shift(hours=200/34 + 200/32).isoformat()
    assert open_time(481, 400, begintime) == False
    assert open_time(720, 600, begintime) == begintime.shift(hours=200/34 + 200/32 + 200/30).isoformat()
    assert open_time(721, 600, begintime) == False
    assert open_time(1200, 1000, begintime) == begintime.shift(hours=200/34 + 200/32 + 200/30 + 400/28).isoformat()
    assert open_time(1201, 1000, begintime) == False
