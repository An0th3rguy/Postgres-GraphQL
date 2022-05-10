# Code in this cell is just for (re)starting the API on a Process, and other compatibility stuff with Jupyter cells.
# Just ignore it!
import uvicorn
from multiprocessing import Process
import starlette_graphene3
import graphene

from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship

from sqlalchemy_utils.functions import database_exists, create_database


# servers = {}
# _api_process = None

# def start_api(app=None, port=9992, runNew=True):
#     """Stop the API if running; Start the API; Wait until API (port) is available (reachable)"""
#     assert port in [9991, 9992, 9993, 9994], f'port has unexpected value {port}'
#     def run():
#         uvicorn.run(app, port=port, host='0.0.0.0', root_path='')    
        
#     _api_process = servers.get(port, None)
#     if _api_process:
#         _api_process.terminate()
#         _api_process.join()
#         del servers[port]
    
#     if runNew:
#         assert (not app is None), 'app is None'
#         _api_process = Process(target=run, daemon=True)
#         _api_process.start()
#         servers[port] = _api_process


BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')

UserGroupModel = Table('users_groups', BaseModel.metadata,
        Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
        Column('user_id', ForeignKey('users.id'), primary_key=True),
        Column('group_id', ForeignKey('groups.id'), primary_key=True)
)

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)

    groups = relationship('GroupModel', secondary=UserGroupModel, back_populates='users')
        
class GroupModel(BaseModel):
    __tablename__ = 'groups'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)
    entryYearId = Column(Integer)

    externalId = Column(String, index=True)

    grouptype_id = Column(ForeignKey('grouptypes.id'))
    grouptype = relationship('GroupTypeModel', back_populates='groups')

    users = relationship('UserModel', secondary=UserGroupModel, back_populates='groups')

class GroupTypeModel(BaseModel):
    __tablename__ = 'grouptypes'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    groups = relationship('GroupModel', back_populates='grouptype')



connectionstring = 'postgresql+psycopg2://postgres:example@localhost/newdatabase'
engine = create_engine(connectionstring) 


# # BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)


SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()





import graphene

class UserGQL(graphene.ObjectType):
    """Represents an user. User can be connected to several groups where the user is member. Also the user can play several roles."""
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    email = graphene.String()
    
    groups = graphene.Field(graphene.List(lambda: GroupGQL))
    
    def resolve_groups(parent, info):
        return parent.groups
        
class GroupTypeGQL(graphene.ObjectType): 
    """"Represents a type of group such as "faculty" or "department". """
    id = graphene.ID()
    name = graphene.String()
    
    groups = graphene.List(lambda: GroupGQL)   
    
    def resolve_groups(parent, info):
        return parent.groups
    
class GroupGQL(graphene.ObjectType):
    """"Represents a group which has several members - users. Group is defined by its type, also it has a parent and children."""
    id = graphene.ID()
    name = graphene.String()
    users = graphene.List(UserGQL)
    
    def resolve_users(parent, info):
        return parent.users

    grouptype = graphene.Field(lambda: GroupTypeGQL)
    
    def resolve_grouptype(parent, info):
        groupTypeId = parent.grouptype_id
        ###
        return parent.grouptype


class QueryGQL(graphene.ObjectType):
    user = graphene.Field(UserGQL, id = graphene.ID(required = True))
    group = graphene.Field(GroupGQL, id = graphene.ID(required = True))
    grouptype = graphene.Field(GroupTypeGQL, id = graphene.ID(required = True))
    
    def resolve_user(root, info, id):
        session = extractSession(info)
        result = session.query(UserModel).filter(UserModel.id==id).first()
        return result
    
    def resolve_group(root, info, id):
        session = extractSession(info)
        result = session.query(GroupModel).filter(GroupModel.id==id).first()
        return result    
    
    def resolve_grouptype(root, info, id):
        session = extractSession(info)
        result = session.query(GroupTypeModel).filter(GroupTypeModel.id==id).first()
        return result






import graphene

class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=False)
    surname = graphene.String(required=False)
    email = graphene.String(required=False)
    
    def asDict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'email': self.email
        }
    
class CreateUserGQL(graphene.Mutation):
    class Arguments:
        user = CreateUserInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(UserGQL)
    
    def mutate(parent, info, user):
        session = extractSession(info)
        userDict = user.asDict()
        userRow = UserModel(**userDict)
        session.add(userRow)
        session.commit()
        session.refresh(userRow)
        return CreateUserGQL(ok=True, result=userRow)
    pass

class UpdateUserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    surname = graphene.String(required=False)
    email = graphene.String(required=False)
    
    def asDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email
        }
    
class UpdateUserGQL(graphene.Mutation):
    class Arguments:
        user = UpdateUserInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(UserGQL)
    
    def mutate(parent, info, user):
        session = extractSession(info)
        userDict = user.asDict()
        userRow = session.query(UserModel).filter(UserModel.id==user.id).first()
        if 'name' in userDict and userDict['name'] != None:
            userRow.name = userDict['name']
        if 'surname' in userDict and userDict['surname'] != None:
            userRow.surname = userDict['surname']
        if 'email' in userDict and userDict['email'] != None:
            userRow.email = userDict['email']
        # session.add(userDict)
        session.commit()
        session.refresh(userRow)
        return CreateUserGQL(ok=True, result=userRow)
    pass


class Mutations(graphene.ObjectType):
    create_user = CreateUserGQL.Field()
    update_user = UpdateUserGQL.Field()



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

#from starlette.graphql import GraphQLApp
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

import graphene
from fastapi import FastAPI

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL, mutation=Mutations), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app)
# start_api(app=app, port=9992, runNew=True)
uvicorn.run(app, port=9992, host='0.0.0.0', root_path='')