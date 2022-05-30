import string
from datetime import datetime
from random import choices
from .extensions import db

class Link(db.Model):
    #first col is integer col, for primary key
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(5), unique=True)
    # visits
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())

    ## kwargs: keyword arguments, with flask sqlalchemy, when creating an object using a class that's a model, pass in cols that you want to set in the beginning
    def __init__(self, **kwargs):
        #calling this on model
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()
     
    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        #check if short_url is unique in db
        link = self.query.filter_by(short_url=short_url).first()
        #if link exists, then call the method again and try
        if link:
            #recursive call
            return self.generate_short_link()
        else:
            return short_url

    def __repr__(self):
        return '<Link %r>' % self.url
