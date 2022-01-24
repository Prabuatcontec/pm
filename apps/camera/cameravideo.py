# camera.py
# import the necessary packages
import cv2
import pickle
import os
import time, datetime, calendar
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from apps.report.models import motions





class VideoDataCamera(object):
    def __init__(self):
        # capturing video rtsp://admin:contec23@10.10.153.21:8221/Streaming/Channels/102/picture?subtype=1
        # "rtsp://admin:3J7Bm!j@@10.10.153.13/doc/page/preview.asp"
        self.video = cv2.VideoCapture("rtsp://admin:3J7Bm!j@@10.10.153.21:8221/Streaming/Channels/102/picture?subtype=1")
        ret, self.frame1 = self.video.read()
        ret, self.frame2 = self.video.read()
        self.frame1 = cv2.resize(self.frame1, (1100, 700), interpolation=cv2.INTER_AREA)
        self.frame2 = cv2.resize(self.frame2, (1100, 700), interpolation=cv2.INTER_AREA)

        self.motions = []

    def __del__(self):
        # releasing camera
        self.video.release()


    def get_frame(self):

        diff = cv2.absdiff(self.frame1, self.frame2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        movementPoints = []
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 50:
                continue
            movementPoints.append([x, y])
            cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (255, 255, 0), 2)


        listStation = self.get_station_config()
        for station in listStation:


            arrayassign = []
            i = 0
            for key  in  station['location']:
                arrayassign.append(station['location'][key])
                i = i + 1
            i = 0
            oldX = 0
            oldY = 0
            for key in arrayassign:

                if i != 0:
                    cv2.rectangle(self.frame1, (oldX, oldY),
                             (key[0], key[1]), (0, 255, 0),
                             thickness=1)
                    cv2.putText(self.frame1, station['name'], (oldX-10, oldY-10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 1)
                i = i + 1
                oldX = key[0]
                oldY = key[1]

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', self.frame1)
        self.motions = []
        self.frame1 = self.frame2
        ret, self.frame2 = self.video.read()
        if ret:
            self.frame2 = cv2.resize(self.frame2, (1100, 700), interpolation=cv2.INTER_AREA)
        else:

            self.video.release()
            self.video = cv2.VideoCapture(self.cred)
            ret, self.frame2 = self.video.read()
            self.frame2 = cv2.resize(self.frame2, (1100, 700), interpolation=cv2.INTER_AREA)
        return jpeg.tobytes()

    def get_station_config(self):
        try:
            data = pickle.load(open(get_correct_path("stationConfig.p"), "rb"))
        except EOFError:
            data = list()
        return data



def get_correct_path(relative_path):
    p = os.path.abspath(".").replace('/dist', "")
    return os.path.join(p, relative_path)

