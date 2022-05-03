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


connectionstring = 'postgresql+psycopg2://postgres:example@localhost/database99'

if not database_exists(connectionstring):  # => False
    try:
        create_database(connectionstring)
        doCreateAll = True
        print('Database created')
    except Exception as e:
        print('Database does not exists and cannot be created')
        raise
else:
    print('Database already exists')




BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')

class Notebook_Vendor(BaseModel):
    __tablename__ = 'NotebookVendor'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    notebook_id = Column(ForeignKey('Notebook.id'), primary_key=True)
    vendor_id = Column(ForeignKey('Vendors.id'), primary_key=True)
    stock = Column(String)
    quantity = Column(String)
    price = Column(String)


    vendors = relationship('Vendor', back_populates='notebooks')
    notebook = relationship('Notebook', back_populates='vendors')


class Notebook(BaseModel):
    __tablename__ = 'Notebook'

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

    brand_id = Column(Integer, ForeignKey('Brands.id'))
    brands = relationship("Brand", back_populates='notebooks02')

    lastchange = Column(DateTime, default=datetime.datetime.now)
    # externalId = Column(BigInteger, index=True)

    # Vendors = relationship('Vendor', secondary=Notebook_Vendor, back_populates='Notebook')
    vendors = relationship('Notebook_Vendor', back_populates = 'notebook')


class Vendor(BaseModel):
    __tablename__ = 'Vendors'

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
    notebooks = relationship('Notebook_Vendor', back_populates = 'vendors')


class Brand(BaseModel):
    __tablename__ = 'Brands'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    headquarter = Column(String)
    established = Column(String)
    web = Column(String)

    notebooks02 = relationship("Notebook", back_populates='brands')


    # groups = relationship('GroupModel', back_populates='grouptype')


#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()





class NotebookGQL(graphene.ObjectType):
    """Represents an user. User can be connected to several groups where the user is member. Also the user can play several roles."""
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    email = graphene.String()
    
    groups = graphene.Field(graphene.List(lambda: GroupGQL))
    
    def resolve_groups(parent, info):
        return parent.groups
        
class VendorGQL(graphene.ObjectType): 
    """"Represents a type of group such as "faculty" or "department". """
    id = graphene.ID()
    name = graphene.String()
    
    groups = graphene.List(lambda: GroupGQL)   
    
    def resolve_groups(parent, info):
        return parent.groups
    
class BrandGQL(graphene.ObjectType):
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