from fastapi import FastAPI
import uvicorn
import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from session import SessionMaker, defineStartupAndShutdown

from queries import QueryGQL
from mutations import Mutations

# ###########################
# Fast API
# ###########################

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL, mutation=Mutations), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app)
# start_api(app=app, port=9992, runNew=True)
uvicorn.run(app, port=9992, host='0.0.0.0', root_path='')