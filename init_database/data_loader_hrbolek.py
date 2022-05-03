#https://docs.sqlalchemy.org/en/13/orm/tutorial.html
#https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, Sequence, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy_utils.functions import database_exists, create_database

connectionstring = 'postgresql+psycopg2://postgres:example@localhost/newdatabase'
if not database_exists(connectionstring):  #=> False
    try:
        create_database(connectionstring)
        doCreateAll = True
        print('Database created')
    except Exception as e:
        print('Database does not exists and cannot be created')
        raise
else:
    print('Database already exists')

from sqlalchemy import create_engine

#engine = create_engine('sqlite:///:memory:', echo=True)
#engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')

engine = create_engine(connectionstring) 

from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

import datetime
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship

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

#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

def crudUserGet(db: SessionMaker, id: int):
    return db.query(UserModel).filter(UserModel.id==id).first()

def crudUserGetAll(db: SessionMaker, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def crudUserCreate(db: SessionMaker, user):
    userRow = UserModel(name=user.name, surname=user.surname, email=user.email, externalId=user.externalId)
    db.add(userRow)
    db.commit()
    db.refresh(userRow)
    return userRow

def crudUserUpdate(db: SessionMaker, user):
    userToUpdate = db.query(UserModel).filter(UserModel.id==user.id).first()
    userToUpdate.name = user.name if user.name else userToUpdate.name
    userToUpdate.surname = user.surname if user.surname else userToUpdate.surname
    userToUpdate.email = user.email if user.email else userToUpdate.email
    db.commit()
    db.refresh(userToUpdate)
    return userToUpdate

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}

def crudGroupGet(db: SessionMaker, id: int):
    return db.query(groupModel).filter(groupModel.id==id).first()

def crudGroupGetAll(db: SessionMaker, skip: int = 0, limit: int = 100):
    return db.query(groupModel).offset(skip).limit(limit).all()

def crudGroupCreate(db: SessionMaker, group):
    groupRow = GroupModel(name=group.name, externalId=group.externalId)
    db.add(groupRow)
    db.commit()
    db.refresh(groupRow)
    return groupRow

def crudGroupUpdate(db: SessionMaker, group):
    groupToUpdate = db.query(groupModel).filter(GroupModel.id==group.id).first()
    groupToUpdate.name = group.name if group.name else groupToUpdate.name
    db.commit()
    db.refresh(groupToUpdate)
    return groupToUpdate

def linkUserToGroup(db: SessionMaker, userId, groupId):
    groupRow = db.query(GroupModel).filter(GroupModel.id==groupId).first()
    userRow = db.query(UserModel).filter(UserModel.id==userId).first()
    userRow.groups.append(groupRow)
    db.commit()
    return None    

import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    return result 

def randomUser():
    surNames = [
        'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
        'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý', 
        'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
        'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová', 
        'Marková', 'Němec', 'Pokorná', 'Pospíšilová','Marek'
    ]

    names = [
        'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
        'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
        'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
        'Michal', 'František', 'Lenka', 'Kateřina',
        'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
    ]

    name1 = random.choice(names)
    name2 = random.choice(names)
    name3 = random.choice(surNames)
    return {'name': f'{name1} {name2}', 'surname': f'{name3}', 'email': f'{name1}.{name2}.{name3}@university.world'}

def PopulateUsers(count=10, group=None):
    for i in range(count):
        userNames = randomUser()
        crudUserCreate(db=session, user=UserModel(**userNames))
        
session = SessionMaker()
PopulateUsers(10)
session.close()
