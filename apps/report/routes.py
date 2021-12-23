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


@blueprint.route('/report')
@login_required
def report():
    autoids = autoid().request_loader()
    if autoids != None:
        upautoidlastValue = autoids.value #33966071
    response = requests.get('https://deepbluapi.gocontec.com/autoreceive/direct-shipments?id=' + str(upautoidlastValue),
                            headers={'Content-Type': 'application/json',
                                     'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM='}
                            )
    if response.status_code == 200:
        print("resp")
        print(response.content.decode("utf-8"))
        print("=========")

        if (response.content.decode("utf-8") != ""):
            print("=========DDDDDD")
            result = response.json()
            print(result)
            for value in result:
                print('IN')
                values = {"scantime": value["Scan Timestamp"],
                          "station": value["Work Station ID"],
                          "operator": value["Operator ID"],
                          "product": value["Product ID"],
                          "eventtype": value["Event Type"],
                          "shipid": value["Shipment ID"],
                          "errorcode": value["Error Code"],
                          "errormessage": value["Error Message"]}
                motions.add_data(values)



            db.session.query(autoid).filter(autoid.id == autoids.id).update(
                {'value': len(result) + int(upautoidlastValue)})
            db.session.commit()

    stationTime = motions.motion_loader_byarea('Line2Station')
    time_report_count = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "10-15": 0, "60-480": 0}
    time_report = {"1-2": 0, "2-3": 0, "3-5": 0, "5-10": 0, "10-15": 0, "10-15": 0, "60-480": 0}
    totalAway = 0
    print(stationTime)
    for station in stationTime:
        if station[5] <= 120:
            p_time = time_report["1-2"]
            time_report_count["1-2"] = int(time_report_count["1-2"]) + 1
            time_report["1-2"] = (int(p_time) + station[5])
        if 120 < station[5] <= 180:
            p_time = time_report["2-3"]
            time_report_count["2-3"] = int(time_report_count["2-3"]) + 1
            time_report["2-3"] = (int(p_time) + station[5])

        if 180 < station[5] <= 300:
            p_time = time_report["3-5"]
            time_report_count["3-5"] = int(time_report_count["3-5"]) + 1
            time_report["3-5"] = (int(p_time) + station[5])

        if 300 < station[5] <= 600:
            p_time = time_report["5-10"]
            time_report_count["5-10"] = int(time_report_count["5-10"]) + 1
            time_report["5-10"] = (int(p_time) + station[5])

        if 600 < station[5] <= 14400:
            p_time = time_report["5-10"]
            time_report_count["5-10"] = int(time_report_count["5-10"]) + 1
            time_report["5-10"] = (int(p_time) + station[5])

    result = {'totaltime': time_report, 'count': time_report_count}
    return jsonify(result), 200



