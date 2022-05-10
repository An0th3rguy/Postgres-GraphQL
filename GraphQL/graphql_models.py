import graphene

# ###########################
# GraphQL MODELS
# ###########################

class NotebookVendorGQL(graphene.ObjectType):
    """"Represents a group which has several members - users. Group is defined by its type, also it has a parent and children."""
    id = graphene.ID()
    notebook_id = graphene.ID()
    vendor_id = graphene.ID()
    stock = graphene.String()
    quantity = graphene.String()
    price = graphene.String()

    notebook = graphene.Field(lambda: NotebookGQL)

    def resolve_notebook(parent, info):
        return parent.notebook

    vendor = graphene.Field(lambda: VendorGQL)
    
    def resolve_vendor(parent, info):
        return parent.vendor



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

    
    brand = graphene.Field(lambda: BrandGQL)
    
    def resolve_brand(parent, info):
        #brandID = parent.brand_id
        ###
        return parent.brand

    lastchange = graphene.DateTime()

    prices = graphene.List(lambda: NotebookVendorGQL)
    
    def resolve_prices(parent, info):
        
        return parent.prices
    
    
        
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


    products = graphene.List(lambda: NotebookVendorGQL)   
    
    def resolve_products(parent, info):
        return parent.products
    
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
