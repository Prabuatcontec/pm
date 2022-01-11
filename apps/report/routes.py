# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import jsonify, session, make_response
from apps.home import blueprint
from flask import render_template, request, Response
import requests
from flask_login import login_required
from apps.report.models import motions
from apps.camera.autoid import autoid
from apps import db
import csv
from datetime import datetime, timedelta


@blueprint.route('/report/box')
@login_required
def report_box():
    stationBox = {"Line1Station": "box1", "Line2Station": "box2", "Line3Station": "box3","Line4Station": "box4"}
    stationTime = motions.actionin_box_area(stationBox[session['search_station']])
    time_report_count = {}
    time_report = {}
    time_report_hrs = {}
    # "1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0
    totalAway = 0

    station_all_day = {}
    for station in stationTime:
        dt_obj = datetime.fromtimestamp(station[0]).strftime('%d-%m-%Y')
        if dt_obj not in time_report_count:
            time_report_count[dt_obj] = {"1-2": 0}
            time_report[dt_obj] = {"1-2": 0}
            time_report_hrs[dt_obj] = {"1-2": 0}

        if station[5] > 0:
            p_time = time_report[dt_obj]["1-2"]
            time_report_count[dt_obj]["1-2"] = int(time_report_count[dt_obj]["1-2"]) + 1
            time_report[dt_obj]["1-2"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["1-2"] = convert_time((int(p_time) + station[5]))

    station_all_day = {"time_report_count": time_report_count, "time_report": time_report,
                       "time_report_hrs": time_report_hrs}

    result = {'result': station_all_day}

    return jsonify(result), 200


@blueprint.route('/report/shipping')
@login_required
def report_shipping():
    stationDis = {"Line1Station": "CLD-SHIP13", "Line2Station": "CLD-SHIP15","Line3Station": "CLD-SHIP16","Line4Station": "CLD-SHIP21"}

    stationTime = motions.actionin_shipping_data(stationDis[session['search_station']])
    time_report_count = {}
    time_report = {}
    time_report_hrs = {}
    pretime = {}
    hrShippingCount = {}
    totalAway = 0

    station_all_day = {}
    for station in stationTime:

        dt_obj = datetime.fromtimestamp(station[3]).strftime('%d-%m-%Y')

        if dt_obj not in time_report_count:
            time_report_count[dt_obj] = {"0-1": 0, "1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report[dt_obj] = {"0-1": 0, "1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report_hrs[dt_obj] = {"0-1": 0, "1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            pretime[dt_obj] = 0
            hrShippingCount[dt_obj] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                                       8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0,
                                       20: 0,
                                       21: 0, 22: 0, 23: 0}

        hrShippingCount[dt_obj][int(station[4])] = hrShippingCount[dt_obj][int(station[4])] + 1
        if pretime[dt_obj] < int(station[3]) or pretime[dt_obj] == 0:
            pretime[dt_obj] = int(station[3])
        if int(station[2]) < 60:
            p_time = time_report[dt_obj]["0-1"]
            time_report_count[dt_obj]["0-1"] = int(time_report_count[dt_obj]["0-1"]) + 1
            time_report[dt_obj]["0-1"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["0-1"] = convert_time((int(p_time) + int(station[2])))

        if 59 < int(station[2]) <= 120:
            p_time = time_report[dt_obj]["1-2"]
            time_report_count[dt_obj]["1-2"] = int(time_report_count[dt_obj]["1-2"]) + 1
            time_report[dt_obj]["1-2"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["1-2"] = convert_time((int(p_time) + int(station[2])))
        if 120 < int(station[2]) <= 180:
            p_time = time_report[dt_obj]["2-3"]
            time_report_count[dt_obj]["2-3"] = int(time_report_count[dt_obj]["2-3"]) + 1
            time_report[dt_obj]["2-3"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["2-3"] = convert_time((int(p_time) + int(station[2])))

        if 180 < int(station[2]) <= 300:
            p_time = time_report[dt_obj]["3-5"]
            time_report_count[dt_obj]["3-5"] = int(time_report_count[dt_obj]["3-5"]) + 1
            time_report[dt_obj]["3-5"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["3-5"] = convert_time((int(p_time) + int(station[2])))

        if 300 < int(station[2]) <= 600:
            p_time = time_report[dt_obj]["5-10"]
            time_report_count[dt_obj]["5-10"] = int(time_report_count[dt_obj]["5-10"]) + 1
            time_report[dt_obj]["5-10"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["5-10"] = convert_time((int(p_time) + int(station[2])))

        if 600 < int(station[2]) <= 900:
            p_time = time_report[dt_obj]["10-15"]
            time_report_count[dt_obj]["10-15"] = int(time_report_count[dt_obj]["10-15"]) + 1
            time_report[dt_obj]["10-15"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["10-15"] = convert_time((int(p_time) + int(station[2])))

        if 900 < int(station[2]) <= 3600:
            p_time = time_report[dt_obj]["15-60"]
            time_report_count[dt_obj]["15-60"] = int(time_report_count[dt_obj]["15-60"]) + 1
            time_report[dt_obj]["15-60"] = (int(p_time) + int(station[2]))
            time_report_hrs[dt_obj]["15-60"] = convert_time((int(p_time) + int(station[2])))

    station_all_day = {"time_report_count": time_report_count,
                       "time_report": time_report,
                       "time_report_hrs": time_report_hrs,
                       "pretime": pretime,
                       "hrShippingCount": hrShippingCount}


    session['hrShippingCount'] = hrShippingCount

    result = {'result': station_all_day}
    return jsonify(result), 200

@blueprint.route('/report-csv')
@login_required
def report_csv():
    now = datetime.now()

    fields_csv = 'Date, 1-2 Min,2-3 Min,3-5 Min,5-10 Min,10-15 Min,15-60 Min\n'
    rows = ["1-2", "2-3", "3-5", "5-10", "10-15", "15-60"]
    time_report_count_csv = session['time_report_count']
    #print(time_report_count_csv)
    for x in range(7):
        d = now - timedelta(days=x)

        if d.strftime("%d-%m-%Y") not in time_report_count_csv:
            time_report_count_csv[d.strftime("%d-%m-%Y")] = {  "1-2": 0, "2-3": 0,
                                                             "3-5": 0, "5-10": 0, "10-15": 0,
                                                             "15-60": 0}
        for i, val in enumerate(rows):
            if val not in time_report_count_csv[d.strftime("%d-%m-%Y")]:
                time_report_count_csv[d.strftime("%d-%m-%Y")][val] = 0

        fields_csv += d.strftime("%d-%m-%Y")+','+str(time_report_count_csv[d.strftime("%d-%m-%Y")]["1-2"])+','+str(time_report_count_csv[d.strftime("%d-%m-%Y")]["2-3"])\
                      +','+str(time_report_count_csv[d.strftime("%d-%m-%Y")]["3-5"])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]["5-10"])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]["10-15"])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]["15-60"])+'\n\n\n';

        time_report_time = session['time_report_time']

    for x in range(7):
        d = now - timedelta(days=x)
        if d.strftime("%d-%m-%Y") not in time_report_time:
            time_report_time[d.strftime("%d-%m-%Y")] = {  "1-2": [], "2-3": [],
                                                             "3-5": [], "5-10": [], "10-15": [],
                                                             "15-60": []}


        for i, val in enumerate(rows):
            if val not in time_report_time[d.strftime("%d-%m-%Y")]:
                time_report_time[d.strftime("%d-%m-%Y")][val] = []
        for o,data  in enumerate(rows):
            fields_csv += '\n'+d.strftime("%d-%m-%Y") + '\n'
            for i, val in enumerate(time_report_time[d.strftime("%d-%m-%Y")][data]):
                fields_csv += str(val["from"]) + "," + str(val["to"]) + ",,"




    response = make_response(fields_csv)
    cd = 'attachment; filename=Shipment'+str(now)+'.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response


@blueprint.route('/report-csv-op-activity')
@login_required
def report_csv_op_activity():
    now = datetime.now()

    fields_csv = 'Date,0 Hr,1 Hr,2 Hr,3 Hr,4 Hr,5 Hr,6 Hr,7 Hr,8 Hr,9 Hr,10 Hr,11 Hr,12 Hr,13 Hr,14 Hr,15 Hr,16 Hr,17 Hr,18 Hr,' \
                 '19 Hr,20 Hr,21 Hr,22 Hr,23 Hr\n'
    rows = []
    time_report_count_csv = session['hrShippingCount']

    for x in range(7):
        d = now - timedelta(days=x)

        if d.strftime("%d-%m-%Y") not in time_report_count_csv:
            time_report_count_csv[d.strftime("%d-%m-%Y")] = {'0': 0, '1': 0, '2': 0,
                                                             '3': 0, '4': 0, '5': 0,
                                                             '6': 0, '7': 0, '8': 0,
                                                             '9': 0, '10': 0, '11': 0,
                                                             '12': 0, '13': 0, '14': 0,
                                                             '15': 0, '16': 0, '17': 0,
                                                             '18': 0, '19': 0, '20': 0,
                                                             '21': 0, '22': 0, '23': 0}

        fields_csv += d.strftime("%d-%m-%Y")+','+ str(time_report_count_csv[d.strftime("%d-%m-%Y")]['0'])+','\
                      +str(time_report_count_csv[d.strftime("%d-%m-%Y")]['1'])+','\
                      +str(time_report_count_csv[d.strftime("%d-%m-%Y")]['2'])\
                      +','+str(time_report_count_csv[d.strftime("%d-%m-%Y")]['3'])+',' +\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['4'])+',' +\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['5'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['6'])+',' +\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['7'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['8'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['9'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['10'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['11'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['12'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['13'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['14'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['15'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['16'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['17'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['18'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['19'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['20'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['21'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['22'])+','+\
                      str(time_report_count_csv[d.strftime("%d-%m-%Y")]['23'])+'\n';



    response = make_response(fields_csv)
    cd = 'attachment; filename=Operator_shipment_hours_'+str(now)+'.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response

@blueprint.route('/report')
@login_required
def report():

    stationTime = motions.motion_loader_byarea(session['search_station'])
    time_report_count = {}
    time_report = {}
    time_report_hrs = {}
    time_report_time = {}
    pretime = {}

    station_all_day = {}
    for station in stationTime:

        dt_obj = datetime.fromtimestamp(station[0]).strftime('%d-%m-%Y')
        if dt_obj not in time_report_count:
            time_report_count[dt_obj] = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report[dt_obj] = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report_hrs[dt_obj] = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report_time[dt_obj] = {"1-2": [], "2-3": [], "3-5": [], "5-10": [], "10-15": [], "15-60": []}
            pretime[dt_obj] = 0
        if pretime[dt_obj] < int(station[0]) or pretime[dt_obj] == 0:
            pretime[dt_obj] = int(station[0])
        if 59 < station[5] <= 120:
            p_time = time_report[dt_obj]["1-2"]
            time_report_count[dt_obj]["1-2"] = int(time_report_count[dt_obj]["1-2"]) + 1
            time_report[dt_obj]["1-2"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["1-2"] = convert_time((int(p_time) + station[5]))
            time_report_time[dt_obj]["1-2"].append({"from": datetime.fromtimestamp(int(station[0])),
                                                    "to": datetime.fromtimestamp(int(station[4]))})
        if 120 < station[5] <= 180:
            p_time = time_report[dt_obj]["2-3"]
            time_report_count[dt_obj]["2-3"] = int(time_report_count[dt_obj]["2-3"]) + 1
            time_report[dt_obj]["2-3"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["2-3"] = convert_time((int(p_time) + station[5]))
            time_report_time[dt_obj]["2-3"].append({"from": datetime.fromtimestamp(int(station[0])),
                                                    "to": datetime.fromtimestamp(int(station[4]))})
        if 180 < station[5] <= 300:
            p_time = time_report[dt_obj]["3-5"]
            time_report_count[dt_obj]["3-5"] = int(time_report_count[dt_obj]["3-5"]) + 1
            time_report[dt_obj]["3-5"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["3-5"] = convert_time((int(p_time) + station[5]))
            time_report_time[dt_obj]["3-5"].append({"from": datetime.fromtimestamp(int(station[0])),
                                                    "to": datetime.fromtimestamp(int(station[4]))})

        if 300 < station[5] <= 600:
            p_time = time_report[dt_obj]["5-10"]
            time_report_count[dt_obj]["5-10"] = int(time_report_count[dt_obj]["5-10"]) + 1
            time_report[dt_obj]["5-10"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["5-10"] = convert_time((int(p_time) + station[5]))
            time_report_time[dt_obj]["5-10"].append({"from": datetime.fromtimestamp(int(station[0])),
                                                    "to": datetime.fromtimestamp(int(station[4]))})

        if 600 < station[5] <= 900:
            p_time = time_report[dt_obj]["10-15"]
            time_report_count[dt_obj]["10-15"] = int(time_report_count[dt_obj]["10-15"]) + 1
            time_report[dt_obj]["10-15"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["10-15"] = convert_time((int(p_time) + station[5]))
            time_report_time[dt_obj]["10-15"].append({"from": datetime.fromtimestamp(int(station[0])),
                                                    "to": datetime.fromtimestamp(int(station[4]))})

        if 900 < station[5] <= 1000:
            p_time = time_report[dt_obj]["15-60"]
            time_report_count[dt_obj]["15-60"] = int(time_report_count[dt_obj]["15-60"]) + 1
            time_report[dt_obj]["15-60"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["15-60"] = convert_time((int(p_time) + station[5]))
            time_report_time[dt_obj]["15-60"].append({"from": datetime.fromtimestamp(int(station[0])),
                                                    "to": datetime.fromtimestamp(int(station[4]))})

    #print(time_report_time)
    station_all_day = {"time_report_count": time_report_count, "time_report": time_report,
                       "time_report_hrs": time_report_hrs, "pretime": pretime}

    result = {'result': station_all_day}

    session['time_report_count'] = time_report_hrs
    session['time_report_time'] = time_report_time
    return jsonify(result), 200


def convert_time(seconds):
    return seconds / 60
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)
