# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, Response , request, jsonify, stream_with_context
from apps.camera.camera import VideoCamera

from apps import login_manager
from apps.camera import blueprint
from flask_login import login_required

import pickle
import os


@blueprint.route('/video_feed')
@login_required
def video_feed():
    return Response(stream_with_context(gen(VideoCamera())),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@blueprint.route('/add_station_config', methods=['POST'])
def add_station_config():
    responseBody = {"results": "sdadasd"}
    data = request.get_json()
    s_name = data['s_name']
    o_area = data['o_area']
    stations = []
    listStation =  get_station_config()
    for station in listStation:
        if station['name'] != s_name:
            stations.append(station)

    stations.append({'name': s_name, 'location': o_area})

    print(stations)
    addStationPickle = {}
    addStationPickle = stations
    pickle.dump(addStationPickle, open(get_correct_path("stationConfig.p"), "wb"))
    return jsonify(responseBody), 200


def get_correct_path(relative_path):
    p = os.path.abspath(".").replace('/dist', "")
    return os.path.join(p, relative_path)

def get_station_config():
    try:
        data = pickle.load(open(get_correct_path("stationConfig.p"), "rb"))
    except EOFError:
        data = list()
    return data
# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')