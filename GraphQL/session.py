from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# ###########################
# Session
# ###########################

BaseModel = declarative_base()

connectionstring = 'postgresql+psycopg2://postgres:example@localhost/database99'
engine = create_engine(connectionstring) 

#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)


SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

dbSessionData = {}

def defineStartupAndShutdown(app, SessionMaker):
    @app.on_event("startup")
    async def startup_event():
        session = SessionMaker()
        dbSessionData['session'] = session

    @app.on_event("shutdown")
    def shutdown_event():
        session = dbSessionData.get('session', None)
        if not session is None:
            session.close()

def extractSession(info):
    session = dbSessionData.get('session', None)
    assert not session is None, 'session is not awailable'
    return session