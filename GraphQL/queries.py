import graphene
from session import extractSession
from graphql_models import NotebookGQL, VendorGQL, BrandGQL, NotebookVendorGQL
from sqlalchemy_models import NotebookModel, BrandModel, BrandModel, NotebookVendorModel

# ###########################
# GraphQL QUERIES
# ###########################

class QueryGQL(graphene.ObjectType):

    notebook = graphene.Field(NotebookGQL, id = graphene.ID(required = True))
    vendor = graphene.Field(VendorGQL, id = graphene.ID(required = True))
    brand = graphene.Field(BrandGQL, id = graphene.ID(required = True))
    # notebookAll = graphene.List(NotebookGQL, id = graphene.ID(required = False))
    
    def resolve_notebook(root, info, id):
        session = extractSession(info)
        result = session.query(NotebookModel).filter(NotebookModel.id==id).first()
        return result
    
    def resolve_vendor(root, info, id):
        session = extractSession(info)
        result = session.query(BrandModel).filter(BrandModel.id==id).first()
        return result

    def resolve_brand(root, info, id):
        session = extractSession(info)
        result = session.query(BrandModel).filter(BrandModel.id==id).first()
        return result

    # def resolve_notebookAll(root, info, id):
    #     session = extractSession(info)
    #     #result = session.query(models.NotebookModel).filter(models.NotebookModel.id==id).first()
    #     result = session.query(models.NotebookModel)
    #     return result   
  