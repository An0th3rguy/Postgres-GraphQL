from fastapi import FastAPI
import uvicorn
import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from session import SessionMaker, defineStartupAndShutdown

from queries import QueryGQL
from mutations import Mutations

from fastapi.middleware.cors import CORSMiddleware


# ###########################
# Fast API
# ###########################

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL, mutation=Mutations), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

# we are not using it while working with localhost
origins = [
    "http://enable-ip-to-get-connection.com",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #enable all origins to get it work with localhost, otherwise CORS ERROR
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age=3600,
)


defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app)
# start_api(app=app, port=9992, runNew=True)
uvicorn.run(app, port=9992, host='0.0.0.0', root_path='')