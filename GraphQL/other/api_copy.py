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


BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')

class NotebookVendorModel(BaseModel):
    __tablename__ = 'notebook_vendors'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    notebook_id = Column(ForeignKey('notebooks.id'), primary_key=True)
    vendor_id = Column(ForeignKey('vendors.id'), primary_key=True)
    stock = Column(String)
    quantity = Column(String)
    price = Column(String)


    vendors = relationship('VendorModel', back_populates='notebooks')
    notebooks = relationship('NotebookModel', back_populates='vendors')


class NotebookModel(BaseModel):
    __tablename__ = 'notebooks'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    model = Column(String)
    name = Column(String)
    size = Column(String)
    cpu = Column(String)
    ram = Column(Integer)
    gpu = Column(String)
    resolution = Column(String)
    storage_type = Column(String)
    storage_size = Column(Integer)
    os = Column(String)
    color = Column(String)
    usage = Column(String)

    brand_id = Column(BigInteger, ForeignKey('brands.id'))
    brand = relationship("BrandModel", back_populates='notebooks')

    lastchange = Column(DateTime, default=datetime.datetime.now)
    # externalId = Column(BigInteger, index=True)

    # Vendors = relationship('Vendor', secondary=Notebook_Vendor, back_populates='Notebook')
    vendors = relationship('NotebookVendorModel', back_populates = 'notebooks')


class VendorModel(BaseModel):
    __tablename__ = 'vendors'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    address = Column(String)
    telephone = Column(String)
    ico = Column(Integer)
    web = Column(String)
    email = Column(String)
    score = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)
    # entryYearId = Column(Integer)

    #externalId = Column(String, index=True)

    # grouptype_id = Column(ForeignKey('grouptypes.id'))
    # grouptype = relationship('GroupTypeModel', back_populates='groups')

    # Notebook = relationship('Notebook', secondary=Notebook_Vendor, back_populates='Vendors')
    notebooks = relationship('NotebookVendorModel', back_populates = 'vendors')


class BrandModel(BaseModel):
    __tablename__ = 'brands'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    headquarter = Column(String)
    established = Column(String)
    web = Column(String)

    notebooks = relationship("NotebookModel", back_populates='brand')


    # groups = relationship('GroupModel', back_populates='grouptype')


connectionstring = 'postgresql+psycopg2://postgres:example@localhost/database99'
engine = create_engine(connectionstring) 

#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()





class NotebookGQL(graphene.ObjectType):
    """Represents an user. User can be connected to several groups where the user is member. Also the user can play several roles."""
    

    id = graphene.ID()
    model = graphene.String()
    name = graphene.String()
    size = graphene.String()
    cpu = graphene.String()
    ram = graphene.Int()
    gpu = graphene.String()
    resolution = graphene.String()
    storage_type = graphene.String()
    storage_size = graphene.Int()
    os = graphene.String()
    color = graphene.String()
    usage = graphene.String()

    
    #brands = graphene.Field(graphene.List(lambda: BrandGQL))
    # brands = graphene.List(lambda: BrandGQL)
    brand = graphene.Field(lambda: BrandGQL)
    
    def resolve_brand(parent, info):
        #brandID = parent.brand_id
        ###
        return parent.brand

    lastchange = graphene.DateTime()
    
        
class VendorGQL(graphene.ObjectType): 
    """"Represents a type of group such as "faculty" or "department". """

    id = graphene.ID()
    name = graphene.String()
    address = graphene.String()
    telephone = graphene.String()
    ico = graphene.Int()
    web = graphene.String()
    email = graphene.String()
    score = graphene.String()
    lastchange = graphene.DateTime()

    # groups = graphene.List(lambda: GroupGQL)   
    
    # def resolve_groups(parent, info):
    #     return parent.groups
    
class BrandGQL(graphene.ObjectType):
    """"Represents a group which has several members - users. Group is defined by its type, also it has a parent and children."""
    id = graphene.ID()
    name = graphene.String()
    headquarter = graphene.String()
    established = graphene.String()
    web = graphene.String()

    notebooks = graphene.List(NotebookGQL)
    
    def resolve_notebooks(parent, info):
        return parent.notebooks


    # users = graphene.List(UserGQL)
    
    # def resolve_users(parent, info):
    #     return parent.users

    # grouptype = graphene.Field(lambda: GroupTypeGQL)
    
    # def resolve_grouptype(parent, info):
    #     groupTypeId = parent.grouptype_id
    #     ###
    #     return parent.grouptype


class QueryGQL(graphene.ObjectType):
    # user = graphene.Field(UserGQL, id = graphene.ID(required = True))
    # group = graphene.Field(GroupGQL, id = graphene.ID(required = True))
    # grouptype = graphene.Field(GroupTypeGQL, id = graphene.ID(required = True))
    notebook = graphene.Field(NotebookGQL, id = graphene.ID(required = True))
    brand = graphene.Field(BrandGQL, id = graphene.ID(required = True))
    
    def resolve_notebook(root, info, id):
        session = extractSession(info)
        result = session.query(NotebookModel).filter(NotebookModel.id==id).first()
        return result
    
    def resolve_brand(root, info, id):
        session = extractSession(info)
        result = session.query(BrandModel).filter(BrandModel.id==id).first()
        return result
    
    # def resolve_user(root, info, id):
    #     session = extractSession(info)
    #     result = session.query(UserModel).filter(UserModel.id==id).first()
    #     return result
    
    # def resolve_group(root, info, id):
    #     session = extractSession(info)
    #     result = session.query(GroupModel).filter(GroupModel.id==id).first()
    #     return result    
    
    # def resolve_grouptype(root, info, id):
    #     session = extractSession(info)
    #     result = session.query(GroupTypeModel).filter(GroupTypeModel.id==id).first()
    #     return result

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
    schema=graphene.Schema(query=QueryGQL), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app)
# start_api(app=app, port=9992, runNew=True)
uvicorn.run(app, port=9992, host='0.0.0.0', root_path='')