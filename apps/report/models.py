# -*- encoding: utf-8 -*-
"""
Cop
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()yright (c) 2019 - present AppSeed.us
"""

from apps import db, login_manager
import requests

from apps.authentication.util import hash_pass


class motions(db.Model):

    __tablename__ = 'motions'

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String)
    timeadded = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)

            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]


            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)


    def motion_loader(id):
        return motions.query.filter_by(id=id).first()


    def motion_loader(request):
        station = request.form.get('station')
        stations = motions.query.filter_by(station=station).first()
        db.session.remove()
        return stations if stations else None

    def motion_loader_byarea(area):
        qrl = str("select (select timeadded as  pretimestamp from motions where id < cid   and "
                  "area =  '"+area+"' order by id desc limit 1),(select id as pre_id from "
                   "motions where id < cid  and area = '"+area+"' order by id desc limit 1), "
                    "cid, area,timeadded, timestamp_diff,dd from (select id as cid, area, "
                   "timeadded, timeadded - lag(timeadded) "
                   "over (order by timeadded) as timestamp_diff, "
                   "(to_timestamp(timeadded - lag(timeadded) "
                   "over (order by timeadded)/1000) AT TIME ZONE 'UTC') "
                   "as dd, (to_timestamp(timeadded - lag(timeadded) "
                   "over (order by timeadded)/1000) AT TIME ZONE 'UTC')::timestamp::date as "
                   "ddate from motions where area = '"+area+"' AND  (to_timestamp(timeadded) AT TIME ZONE 'PST') "
                    ">= current_date - 7  order by timeadded ) t where (timestamp_diff < 14400 "
                    "and timestamp_diff > 60) order by timestamp_diff desc")

        stations = db.session.execute(qrl)
        db.session.remove()
        return stations if stations else None

    def actionin_box_area(area):
        qry = str("select (select timeadded as  pretimestamp from motions where id < cid   "
                "and area =  '"+area+"' order by id desc limit 1), "
                "(select id as pre_id from motions where id < cid  and area = '"+area+"' "
                "order by id desc limit 1), cid, area,timeadded, timestamp_diff,dd from "
                "(select id as cid, area, timeadded, timeadded - lag(timeadded) over "
                "(order by timeadded) as timestamp_diff, (to_timestamp(timeadded - lag(timeadded) "
                "over (order by timeadded)/1000) AT TIME ZONE 'UTC') as dd, "
                "(to_timestamp(timeadded - lag(timeadded) over (order by timeadded)/1000) "
                "AT TIME ZONE 'UTC')::timestamp::date as ddate from motions where area = '"+area+"' "
                "AND  (to_timestamp(timeadded) AT TIME ZONE 'PST') >= current_date - 7 order by timeadded ) "
                "t where  (timestamp_diff > 0 and timestamp_diff < 30) order by cid  desc; ")
        box_cnt = db.session.execute(qry)
        db.session.remove()
        return box_cnt if box_cnt else None

    def add_data(values):
        qry = ("INSERT INTO  directshipping (scantime,station,operator,product,eventtype,"
               "shipid,errorcode,errormessage,siteid) VALUES ('"+values['scantime']+"','"+values['station']+"',"
                "'"+values['operator']+"','"+values['product']+"','"+values['eventtype']+"','"+values['shipid']+"'"
                ",'"+values['errorcode']+"','"+values['errormessage']+"','"+str(values['siteid'])+"') ")

        db.session.execute(qry)
        db.session.commit()
        db.session.remove()
        return qry

    def actionin_shipping_data(area):
        qry = str("select cid, station ,timestamp_diff,scantimee,EXTRACT (hour  FROM to_timestamp(scantime, "
                  "'YYYY-MM-DD hh24:mi:ss')::timestamp),to_timestamp(scantimee)::date as dateadded, product ,siteid   from (select DISTINCT shipid, id as cid, station,scantime, EXTRACT "
                  "(epoch  FROM  to_timestamp(scantime, 'YYYY-MM-DD hh24:mi:ss')::timestamp) as scantimee, "
                  "EXTRACT (epoch  FROM  to_timestamp(scantime, 'YYYY-MM-DD hh24:mi:ss')::timestamp) - "
                  "lag(EXTRACT (epoch FROM  to_timestamp(scantime, 'YYYY-MM-DD hh24:mi:ss')::timestamp)) "
                  "over (order by EXTRACT (epoch  FROM  to_timestamp(scantime, 'YYYY-MM-DD hh24:mi:ss')::timestamp)) "
                  "as timestamp_diff, product,siteid from directshipping where station='"+area+"' AND  "
                  "(to_timestamp(EXTRACT (epoch  FROM  to_timestamp(scantime, 'YYYY-MM-DD hh24:mi:ss')::timestamp)) "
                  "AT TIME ZONE 'PST') >= current_date - 7 order by id desc ) t  "
                  "where  (timestamp_diff > 0 ) order by scantimee  desc")

        box_cnt = db.session.execute(qry)
        db.session.remove()
        return box_cnt if box_cnt else None

