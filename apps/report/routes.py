# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import jsonify
from apps.home import blueprint
from flask import render_template, request, Response
import requests
from flask_login import login_required
from apps.report.models import motions
from apps.camera.autoid import autoid
from apps import db

from datetime import datetime


@blueprint.route('/report/box')
@login_required
def report_box():
    stationTime = motions.actionin_box_area('box2')
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
    stationTime = motions.actionin_shipping_data('CLD-SHIP16')
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

    result = {'result': station_all_day}
    return jsonify(result), 200


@blueprint.route('/report')
@login_required
def report():
    autoids = autoid().request_loader()
    # if autoids != None:
    #     upautoidlastValue = autoids.value #33966071
    # response = requests.get('https://deepbluapi.gocontec.com/autoreceive/direct-shipments?_format=json&model=NVG448B&date=2021-12-20&s_time=16:17:00&e_time=18:17:00',
    #                         headers={'Content-Type': 'application/json',
    #                                  'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM='}
    #                         )
    # if response.status_code == 200:
    #     print("resp")
    #     print(response.content.decode("utf-8"))
    #     print("=========")
    #
    #     if (response.content.decode("utf-8") != ""):
    #         print("=========DDDDDD")
    #         result = response.json()
    #         print(result)
    #         for value in result:
    #             print('IN')
    #             values = {"scantime": value["Scan Timestamp"],
    #                       "station": value["Work Station ID"],
    #                       "operator": value["Operator ID"],
    #                       "product": value["Product ID"],
    #                       "eventtype": value["Event Type"],
    #                       "shipid": value["Shipment ID"],
    #                       "errorcode": value["Error Code"],
    #                       "errormessage": value["Error Message"]}
    #             #motions.add_data(values)
    #
    #
    #
    #         db.session.query(autoid).filter(autoid.id == autoids.id).update(
    #             {'value': len(result) + int(upautoidlastValue)})
    #         db.session.commit()

    stationTime = motions.motion_loader_byarea('Line2Station')
    time_report_count = {}
    time_report = {}
    time_report_hrs = {}
    pretime = {}

    station_all_day = {}
    for station in stationTime:
        dt_obj = datetime.fromtimestamp(station[0]).strftime('%d-%m-%Y')
        if dt_obj not in time_report_count:
            time_report_count[dt_obj] = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report[dt_obj] = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            time_report_hrs[dt_obj] = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "15-60": 0}
            pretime[dt_obj] = 0
        if pretime[dt_obj] < int(station[0]) or pretime[dt_obj] == 0:
            pretime[dt_obj] = int(station[0])
        if 59 < station[5] <= 120:
            p_time = time_report[dt_obj]["1-2"]
            time_report_count[dt_obj]["1-2"] = int(time_report_count[dt_obj]["1-2"]) + 1
            time_report[dt_obj]["1-2"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["1-2"] = convert_time((int(p_time) + station[5]))
        if 120 < station[5] <= 180:
            p_time = time_report[dt_obj]["2-3"]
            time_report_count[dt_obj]["2-3"] = int(time_report_count[dt_obj]["2-3"]) + 1
            time_report[dt_obj]["2-3"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["2-3"] = convert_time((int(p_time) + station[5]))

        if 180 < station[5] <= 300:
            p_time = time_report[dt_obj]["3-5"]
            time_report_count[dt_obj]["3-5"] = int(time_report_count[dt_obj]["3-5"]) + 1
            time_report[dt_obj]["3-5"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["3-5"] = convert_time((int(p_time) + station[5]))

        if 300 < station[5] <= 600:
            p_time = time_report[dt_obj]["5-10"]
            time_report_count[dt_obj]["5-10"] = int(time_report_count[dt_obj]["5-10"]) + 1
            time_report[dt_obj]["5-10"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["5-10"] = convert_time((int(p_time) + station[5]))

        if 600 < station[5] <= 900:
            p_time = time_report[dt_obj]["10-15"]
            time_report_count[dt_obj]["10-15"] = int(time_report_count[dt_obj]["10-15"]) + 1
            time_report[dt_obj]["10-15"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["10-15"] = convert_time((int(p_time) + station[5]))

        if 900 < station[5] <= 3600:
            p_time = time_report[dt_obj]["15-60"]
            time_report_count[dt_obj]["15-60"] = int(time_report_count[dt_obj]["15-60"]) + 1
            time_report[dt_obj]["15-60"] = (int(p_time) + station[5])
            time_report_hrs[dt_obj]["15-60"] = convert_time((int(p_time) + station[5]))

    station_all_day = {"time_report_count": time_report_count, "time_report": time_report,
                       "time_report_hrs": time_report_hrs, "pretime": pretime}

    result = {'result': station_all_day}
    return jsonify(result), 200


def convert_time(seconds):
    return seconds / 60
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)
