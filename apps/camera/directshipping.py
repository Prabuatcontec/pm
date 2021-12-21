# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from apps import db

from apps.authentication.util import hash_pass

class directshipping():

    __tablename__ = 'directshipping'

    id = db.Column(db.Integer, primary_key=True)
    scantime = db.Column(db.String(50))
    station = db.Column(db.String(50))
    operator = db.Column(db.String(50))
    operator = db.Column(db.String(50))
    product = db.Column(db.String(50))
    eventtype = db.Column(db.String(50))
    shipid = db.Column(db.String(50))
    errorcode = db.Column(db.String)
    errormessage = db.Column(db.String)

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


    def user_loader(id):
        return directshipping.query.filter_by(id=id).first()


    def request_loader(request):
        station = request.form.get('station')
        stations = directshipping.query.filter_by(station=station).first()
        return stations if stations else None
