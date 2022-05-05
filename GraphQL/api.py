import uvicorn
import graphene

from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

# importing SQLalchemy models
import models


SessionMaker = sessionmaker(bind=models.engine)
session = SessionMaker()

# ###########################
# GraphQL
# ###########################

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

    notebook = graphene.Field(NotebookGQL, id = graphene.ID(required = True))
    brand = graphene.Field(BrandGQL, id = graphene.ID(required = True))
    # notebookAll = graphene.List(NotebookGQL, id = graphene.ID(required = False))
    
    def resolve_notebook(root, info, id):
        session = extractSession(info)
        result = session.query(models.NotebookModel).filter(models.NotebookModel.id==id).first()
        return result
    
    def resolve_brand(root, info, id):
        session = extractSession(info)
        result = session.query(models.BrandModel).filter(models.BrandModel.id==id).first()
        return result

    # def resolve_notebookAll(root, info, id):
    #     session = extractSession(info)
    #     #result = session.query(models.NotebookModel).filter(models.NotebookModel.id==id).first()
    #     result = session.query(models.NotebookModel)
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


# ###########################
# Fast API
# ###########################

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app)
# start_api(app=app, port=9992, runNew=True)
uvicorn.run(app, port=9992, host='0.0.0.0', root_path='')