import graphene
from session import extractSession
from graphql_models import NotebookGQL, VendorGQL, BrandGQL, NotebookVendorGQL
from sqlalchemy_models import NotebookModel, VendorModel, BrandModel, NotebookVendorModel


# ###########################
# GraphQL MUTATIONS
# ###########################



######################################################## Vendor

class CreateVendorInput(graphene.InputObjectType):

    name = graphene.String(required=False)
    address = graphene.String(required=False)
    telephone = graphene.String(required=False)
    ico = graphene.Int(required=False)
    web = graphene.String(required=False)
    email = graphene.String(required=False)
    score = graphene.String(required=False)
    
    def asDict(self):
        return {
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'ico': self.ico,
            'web': self.web,
            'email': self.email,
            'score': self.score
        }

class CreateVendorGQL(graphene.Mutation):
    class Arguments:
        vendor = CreateVendorInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(VendorGQL)
    
    def mutate(parent, info, vendor):
        session = extractSession(info)
        vendorDict = vendor.asDict()
        vendorRow = VendorModel(**vendorDict)
        session.add(vendorRow)
        session.commit()
        session.refresh(vendorRow)
        return CreateVendorGQL(ok=True, result=vendorRow)
    pass


class UpdateVendorInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    address = graphene.String(required=False)
    telephone = graphene.String(required=False)
    ico = graphene.Int(required=False)
    web = graphene.String(required=False)
    email = graphene.String(required=False)
    score = graphene.String(required=False)
    
    def asDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'ico': self.ico,
            'web': self.web,
            'email': self.email,
            'score': self.score
        }
    
class UpdateVendorGQL(graphene.Mutation):
    class Arguments:
        vendor = UpdateVendorInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(VendorGQL)
    
    def mutate(parent, info, vendor):
        session = extractSession(info)
        vendorDict = vendor.asDict()
        vendorRow = session.query(VendorModel).filter(VendorModel.id==vendor.id).first()
        if 'name' in vendorDict and vendorDict['name'] != None:
            vendorRow.name = vendorDict['name']
        if 'address' in vendorDict and vendorDict['address'] != None:
            vendorRow.address = vendorDict['address']
        if 'telephone' in vendorDict and vendorDict['telephone'] != None:
            vendorRow.telephone = vendorDict['telephone']
        if 'ico' in vendorDict and vendorDict['ico'] != None:
            vendorRow.ico = vendorDict['ico']
        if 'web' in vendorDict and vendorDict['web'] != None:
            vendorRow.web = vendorDict['web']
        if 'email' in vendorDict and vendorDict['email'] != None:
            vendorRow.email = vendorDict['email']
        if 'score' in vendorDict and vendorDict['score'] != None:
            vendorRow.score = vendorDict['score']
        
        # session.delete(vendorRow)
        session.commit()     
        session.refresh(vendorRow)
        return CreateVendorGQL(ok=True, result=vendorRow)
    pass

class DeleteVendorInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    
    def asDict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class DeleteVendorGQL(graphene.Mutation):
   
    class Arguments:
        vendor = DeleteVendorInput(required = True)

    ok = graphene.Boolean()
    result = graphene.Field(VendorGQL)

    def mutate(parent, info, vendor):
        session = extractSession(info)
        vendorDict = vendor.asDict()
        vendorRow = session.query(VendorModel).filter(VendorModel.id==vendor.id).first()
        
        session.delete(vendorRow)
        session.commit()     
        return CreateVendorGQL(ok=True, result=vendorRow)
    pass


####################################################### Brand


class CreateBrandInput(graphene.InputObjectType):

    name = graphene.String(required=False)
    headquarter = graphene.String(required=False)
    established = graphene.String(required=False)
    web = graphene.String(required=False)
    
    def asDict(self):
        return {
            'name': self.name,
            'headquarter': self.headquarter,
            'established': self.established,
            'web': self.web
        }

class CreateBrandGQL(graphene.Mutation):
    class Arguments:
        brand = CreateBrandInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(BrandGQL)
    
    def mutate(parent, info, brand):
        session = extractSession(info)
        brandDict = brand.asDict()
        brandRow = BrandModel(**brandDict)
        session.add(brandRow)
        session.commit()
        session.refresh(brandRow)
        return CreateBrandGQL(ok=True, result=brandRow)
    pass


class UpdateBrandInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    headquarter = graphene.String(required=False)
    established = graphene.String(required=False)
    web = graphene.String(required=False)
    
    def asDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'headquarter': self.headquarter,
            'established': self.established,
            'web': self.web
        }
    
class UpdateBrandGQL(graphene.Mutation):
    class Arguments:
        brand = UpdateBrandInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(BrandGQL)
    
    def mutate(parent, info, brand):
        session = extractSession(info)
        brandDict = brand.asDict()
        brandRow = session.query(BrandModel).filter(BrandModel.id==brand.id).first()
        if 'name' in brandDict and brandDict['name'] != None:
            brandRow.name = brandDict['name']
        if 'headquarter' in brandDict and brandDict['headquarter'] != None:
            brandRow.headquarter = brandDict['headquarter']
        if 'established' in brandDict and brandDict['established'] != None:
            brandRow.established = brandDict['established']
        if 'web' in brandDict and brandDict['web'] != None:
            brandRow.web = brandDict['web']
        
        
        # session.delete(vendorRow)
        session.commit()     
        session.refresh(brandRow)
        return CreateBrandGQL(ok=True, result=brandRow)
    pass

class DeleteBrandInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    
    def asDict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class DeleteBrandGQL(graphene.Mutation):
   
    class Arguments:
        brand = DeleteBrandInput(required = True)

    ok = graphene.Boolean()
    result = graphene.Field(VendorGQL)

    def mutate(parent, info, brand):
        session = extractSession(info)
        brandDict = brand.asDict()
        brandRow = session.query(BrandModel).filter(BrandModel.id==brand.id).first()
        
        session.delete(brandRow)
        session.commit()     
        return CreateBrandGQL(ok=True, result=brandRow)
    pass


####################################################### Notebook


class CreateNotebookInput(graphene.InputObjectType):

    model = graphene.String(required=False)
    name = graphene.String(required=False)
    size = graphene.String(required=False)
    cpu = graphene.String(required=False)
    ram = graphene.Int(required=False)
    gpu = graphene.String(required=False)
    resolution = graphene.String(required=False)
    storage_type = graphene.String(required=False)
    storage_size = graphene.Int(required=False)
    os = graphene.String(required=False)
    color = graphene.String(required=False)
    usage = graphene.String(required=False)
    brand_id = graphene.ID(required=False)

    def asDict(self):
        return {
            'model': self.model,
            'name': self.name,
            'size': self.size,
            'cpu': self.cpu,
            'ram': self.ram,
            'gpu': self.gpu,
            'resolution': self.resolution,
            'storage_type': self.storage_type,
            'storage_size': self.storage_size,
            'os': self.os,
            'color': self.color,
            'usage': self.usage,
            'brand_id': self.brand_id
        }

class CreateNotebookGQL(graphene.Mutation):
    class Arguments:
        notebook = CreateNotebookInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(NotebookGQL)
    
    def mutate(parent, info, notebook):
        session = extractSession(info)
        notebookDict = notebook.asDict()
        notebookRow = NotebookModel(**notebookDict)
        session.add(notebookRow)
        session.commit()
        session.refresh(notebookRow)
        return CreateNotebookGQL(ok=True, result=notebookRow)
    pass


class UpdateNotebookInput(graphene.InputObjectType):

    id = graphene.ID(required=True)
    model = graphene.String(required=False)
    name = graphene.String(required=False)
    size = graphene.String(required=False)
    cpu = graphene.String(required=False)
    ram = graphene.Int(required=False)
    gpu = graphene.String(required=False)
    resolution = graphene.String(required=False)
    storage_type = graphene.String(required=False)
    storage_size = graphene.Int(required=False)
    os = graphene.String(required=False)
    color = graphene.String(required=False)
    usage = graphene.String(required=False)
    brand_id = graphene.ID(required=False)
    
    def asDict(self):
        return {
            'model': self.model,
            'name': self.name,
            'size': self.size,
            'cpu': self.cpu,
            'ram': self.ram,
            'gpu': self.gpu,
            'resolution': self.resolution,
            'storage_type': self.storage_type,
            'storage_size': self.storage_size,
            'os': self.os,
            'color': self.color,
            'usage': self.usage,
            'brand_id': self.brand_id
        }
    
class UpdateNotebookGQL(graphene.Mutation):
    class Arguments:
        notebook = UpdateNotebookInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(NotebookGQL)
    
    def mutate(parent, info, notebook):
        session = extractSession(info)
        notebookDict = notebook.asDict()
        notebookRow = session.query(NotebookModel).filter(NotebookModel.id==notebook.id).first()
        if 'model' in notebookDict and notebookDict['model'] != None:
            notebookRow.model = notebookDict['model']
        if 'name' in notebookDict and notebookDict['name'] != None:
            notebookRow.name = notebookDict['name']
        if 'size' in notebookDict and notebookDict['size'] != None:
            notebookRow.size = notebookDict['size']
        if 'cpu' in notebookDict and notebookDict['cpu'] != None:
            notebookRow.cpu = notebookDict['cpu']
        if 'ram' in notebookDict and notebookDict['ram'] != None:
            notebookRow.ram = notebookDict['ram']
        if 'gpu' in notebookDict and notebookDict['gpu'] != None:
            notebookRow.gpu = notebookDict['gpu']
        if 'resolution' in notebookDict and notebookDict['resolution'] != None:
            notebookRow.resolution = notebookDict['resolution']
        if 'storage_type' in notebookDict and notebookDict['storage_type'] != None:
            notebookRow.storage_type = notebookDict['storage_type']
        if 'storage_size' in notebookDict and notebookDict['storage_size'] != None:
            notebookRow.storage_size = notebookDict['storage_size']
        if 'os' in notebookDict and notebookDict['os'] != None:
            notebookRow.os = notebookDict['os']
        if 'color' in notebookDict and notebookDict['color'] != None:
            notebookRow.color = notebookDict['color']
        if 'usage' in notebookDict and notebookDict['usage'] != None:
            notebookRow.usage = notebookDict['usage']
        if 'brand_id' in notebookDict and notebookDict['brand_id'] != None:
            notebookRow.brand_id = notebookDict['brand_id']
        
        # session.delete(vendorRow)
        session.commit()     
        session.refresh(notebookRow)
        return CreateNotebookGQL(ok=True, result=notebookRow)
    pass

class DeleteNotebookInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    
    def asDict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class DeleteNotebookGQL(graphene.Mutation):
   
    class Arguments:
        notebook = DeleteNotebookInput(required = True)

    ok = graphene.Boolean()
    result = graphene.Field(NotebookGQL)

    def mutate(parent, info, notebook):
        session = extractSession(info)
        notebookDict = notebook.asDict()
        notebookRow = session.query(NotebookModel).filter(NotebookModel.id==notebook.id).first()
        
        session.delete(notebookRow)
        session.commit()     
        return CreateNotebookGQL(ok=True, result=notebookRow)
    pass


####################################################### NotebookVendor


class CreateNotebookVendorInput(graphene.InputObjectType):

    notebook_id = graphene.ID(required=False)
    vendor_id = graphene.ID(required=False)
    stock = graphene.String(required=False)
    quantity = graphene.String(required=False)
    price = graphene.String(required=False)
    
    def asDict(self):
        return {
            'notebook_id': self.notebook_id,
            'vendor_id': self.vendor_id,
            'stock': self.stock,
            'quantity': self.quantity,
            'price': self.price
        }

class CreateNotebookVendorGQL(graphene.Mutation):
    class Arguments:
        notebookVendor = CreateNotebookVendorInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(NotebookVendorGQL)
    
    def mutate(parent, info, notebookVendor):
        session = extractSession(info)
        notebookVendorDict = notebookVendor.asDict()
        notebookVendorRow = NotebookVendorModel(**notebookVendorDict)
        session.add(notebookVendorRow)
        session.commit()
        session.refresh(notebookVendorRow)
        return CreateNotebookVendorGQL(ok=True, result=notebookVendorRow)
    pass


class UpdateNotebookVendorInput(graphene.InputObjectType):
    
    id = graphene.ID(required=True)
    notebook_id = graphene.ID(required=False)
    vendor_id = graphene.ID(required=False)
    stock = graphene.String(required=False)
    quantity = graphene.String(required=False)
    price = graphene.String(required=False)
    
    def asDict(self):
        return {
            'notebook_id': self.notebook_id,
            'vendor_id': self.vendor_id,
            'stock': self.stock,
            'quantity': self.quantity,
            'price': self.price
        }
    
class UpdateNotebookVendorGQL(graphene.Mutation):
    class Arguments:
        notebookVendor = UpdateNotebookVendorInput(required = True)
    
    ok = graphene.Boolean()
    result = graphene.Field(NotebookVendorGQL)
    
    def mutate(parent, info, notebokVendor):
        session = extractSession(info)
        notebookVendorDict = notebokVendor.asDict()
        notebookVendorRow = session.query(NotebookVendorModel).filter(NotebookVendorModel.id==notebokVendor.id).first()
        if 'notebook_id' in notebookVendorDict and notebookVendorDict['notebook_id'] != None:
            notebookVendorRow.notebook_id = notebookVendorDict['notebook_id']
        if 'vendor_id' in notebookVendorDict and notebookVendorDict['vendor_id'] != None:
            notebookVendorRow.vendor_id = notebookVendorDict['vendor_id']
        if 'stock' in notebookVendorDict and notebookVendorDict['stock'] != None:
            notebookVendorRow.stock = notebookVendorDict['stock']
        if 'quantity' in notebookVendorDict and notebookVendorDict['quantity'] != None:
            notebookVendorRow.quantity = notebookVendorDict['quantity']
        if 'price' in notebookVendorDict and notebookVendorDict['price'] != None:
            notebookVendorRow.price = notebookVendorDict['price']
        
        # session.delete(vendorRow)
        session.commit()     
        session.refresh(notebookVendorRow)
        return CreateNotebookVendorGQL(ok=True, result=notebookVendorRow)
    pass

class DeleteNotebookVendorInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    
    def asDict(self):
        return {
            'id': self.id
        }

class DeleteNotebookVendorGQL(graphene.Mutation):
   
    class Arguments:
        notebookVendor = DeleteNotebookVendorInput(required = True)

    ok = graphene.Boolean()
    result = graphene.Field(NotebookVendorGQL)

    def mutate(parent, info, notebookVendor):
        session = extractSession(info)
        notebookVendorDict = notebookVendor.asDict()
        notebookVendorRow = session.query(NotebookVendorModel).filter(NotebookVendorModel.id==notebookVendor.id).first()
        
        session.delete(notebookVendorRow)
        session.commit()     
        return CreateNotebookVendorGQL(ok=True, result=notebookVendorRow)
    pass



class Mutations(graphene.ObjectType):
    
    create_notebook = CreateNotebookGQL.Field()
    update_notebook = UpdateNotebookGQL.Field()
    delete_notebook = DeleteNotebookGQL.Field()
 
    create_vendor = CreateVendorGQL.Field()
    update_vendor = UpdateVendorGQL.Field()
    delete_vendor = DeleteVendorGQL.Field()

    create_brand = CreateBrandGQL.Field()
    update_brand = UpdateBrandGQL.Field()
    delete_brand = DeleteBrandGQL.Field()

    create_notebook_vendor = CreateNotebookVendorGQL.Field()
    update_notebook_vendor = UpdateNotebookVendorGQL.Field()
    delete_notebook_vendor = DeleteNotebookVendorGQL.Field()

