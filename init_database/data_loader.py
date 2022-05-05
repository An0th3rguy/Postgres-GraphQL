# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, Sequence, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy_utils.functions import database_exists, create_database

# ###########################
# First Create a database
# ###########################

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


# ##################################
# Create engine a define structure
# ##################################


from sqlalchemy import create_engine

# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')

engine = create_engine(connectionstring)

from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

import datetime
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship


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

    notebooks = relationship('NotebookVendorModel', back_populates = 'vendors')


class BrandModel(BaseModel):
    __tablename__ = 'brands'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    headquarter = Column(String)
    established = Column(String)
    web = Column(String)

    notebooks = relationship("NotebookModel", back_populates='brand')


#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()


# ###########################
# CRUD operations
# ###########################


def crudNotebookCreate(db: SessionMaker, notebook):
    NotebookRow = NotebookModel(id=notebook.id, name=notebook.name, model = notebook.model, size=notebook.size, cpu=notebook.cpu, ram=notebook.ram, gpu=notebook.gpu, resolution=notebook.resolution, storage_type=notebook.storage_type, storage_size=notebook.storage_size, os=notebook.os, color=notebook.color, usage=notebook.usage, brand_id=notebook.brand_id)
    db.add(NotebookRow)
    db.commit()
    db.refresh(NotebookRow)
    return NotebookRow

def crudBrandCreate(db: SessionMaker, brand):
    BrandRow = BrandModel(id=brand.id, name=brand.name, headquarter = brand.headquarter, established=brand.established, web=brand.web)
    db.add(BrandRow)
    db.commit()
    db.refresh(BrandRow)
    return BrandRow

def crudVendorCreate(db: SessionMaker, vendor):
    VendorRow = VendorModel(id=vendor.id, name=vendor.name, address = vendor.address, telephone=vendor.telephone, ico=vendor.ico, web=vendor.web, email=vendor.email, score=vendor.score)
    db.add(VendorRow)
    db.commit()
    db.refresh(VendorRow)
    return VendorRow

def crudNotebook_VendorCreate(db: SessionMaker, notebook_vendor):
    NotebookVendorRow = NotebookVendorModel(notebook_id=notebook_vendor.notebook_id, vendor_id = notebook_vendor.vendor_id, stock=notebook_vendor.stock, quantity=notebook_vendor.quantity, price=notebook_vendor.price)
    db.add(NotebookVendorRow)
    db.commit()
    db.refresh(NotebookVendorRow)
    return NotebookVendorRow


# ###########################
# Parsing from file
# ###########################


with open("init_database/data/Vendor.txt","r") as file:
    for line in file:
        id, name, address, telephone, ico, web, email, score = line.strip().split(",")
        data = {'id': f'{id}', 'name': f'{name}', 'address': f'{address}', 'telephone': f'{telephone}', 'ico': f'{ico}', 'web': f'{web}', 'email': f'{email}', 'score': f'{score}'}
        crudVendorCreate(db=session, vendor=VendorModel(**data))
        print(data)

with open("init_database/data/Brand.txt","r") as file:
    for line in file:
        id, name, headquarter, established, web = line.strip().split(",")
        data = {'id': f'{id}', 'name': f'{name}', 'headquarter': f'{headquarter}', 'established': f'{established}', 'web': f'{web}'}
        crudBrandCreate(db=session, brand=BrandModel(**data))
        print(data)

with open("init_database/data/Notebook.txt","r") as file:
    for line in file:
        id, name, model, size, cpu, ram, gpu, resolution, storage_type, storage_size, os, color, usage, brand_id = line.strip().split(",")
        data = {'id': f'{id}','name': f'{name}', 'model': f'{model}', 'size': f'{size}', 'cpu': f'{cpu}', 'ram': f'{ram}', 'gpu': f'{gpu}', 'resolution': f'{resolution}', 'storage_type': f'{storage_type}', 'storage_size': f'{storage_size}', 'os': f'{os}','color': f'{color}','usage': f'{usage}','brand_id': f'{brand_id}'}
        print(data)
        crudNotebookCreate(db=session, notebook=NotebookModel(**data))

with open("init_database/data/Notebook-Prodejce.txt","r") as file:
    for line in file:
        notebook_id, vendor_id, stock, quantity, price = line.strip().split(",")
        price = f"{(float(price) / 23.5):.0f}" #czk to usd
        data = {'notebook_id': f'{notebook_id}', 'vendor_id': f'{vendor_id}', 'stock': f'{stock}', 'quantity': f'{quantity}', 'price': f'{price}'}
        print(data)
        crudNotebook_VendorCreate(db=session, notebook_vendor=NotebookVendorModel(**data))
        

session = SessionMaker()
session.close()