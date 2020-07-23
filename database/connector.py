from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        #engine = create_engine('sqlite:///games.db?check_same_thread=False', echo=False)
        engine = create_engine('postgres://sajucwjwwkkybr:624e29d1c50f9c8f897428104b8f2d7fccfffc775547261295c813d067d430e3@ec2-54-86-170-8.compute-1.amazonaws.com:5432/d3gv8ngvbc1703')

        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)
