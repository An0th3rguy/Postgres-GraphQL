import datetime
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# ###########################
# SQLalchemy models
# ###########################

BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')

class NotebookVendorModel(BaseModel):
    __tablename__ = 'notebook_vendors'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    notebook_id = Column(BigInteger, ForeignKey('notebooks.id'), primary_key=True)
    vendor_id = Column(BigInteger, ForeignKey('vendors.id'), primary_key=True)
    stock = Column(String)
    quantity = Column(String)
    price = Column(String)

    # works
    # vendors = relationship('VendorModel', back_populates='notebooks')
    # notebooks = relationship('NotebookModel', back_populates='vendors')

    # vendors = relationship("VendorModel", backref="notebooks_notebook_vendors")
    # notebooks = relationship("NotebookModel", backref="vendors_notebook_vendors")

    notebook = relationship("NotebookModel", back_populates='prices')
    vendor = relationship("VendorModel", back_populates="products")


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

    prices = relationship("NotebookVendorModel", back_populates="notebook")

    # works
    # vendors = relationship('NotebookVendorModel', back_populates = 'notebooks')

    # vendors = relationship("VendorModel", secondary="notebook_vendors")
    


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

    products = relationship("NotebookVendorModel", back_populates="vendor")
    # works
    # notebooks = relationship('NotebookVendorModel', back_populates = 'vendors')


class BrandModel(BaseModel):
    __tablename__ = 'brands'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    headquarter = Column(String)
    established = Column(String)
    web = Column(String)

    notebooks = relationship("NotebookModel", back_populates='brand')

# ###########################
# Connection string
# ###########################

connectionstring = 'postgresql+psycopg2://postgres:example@localhost/database99'
engine = create_engine(connectionstring) 

#BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

