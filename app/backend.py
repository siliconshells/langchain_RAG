from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from app.rag_application import retrieve_generate


@strawberry.type
class Query:
    @strawberry.field
    def greetings(self) -> str:
        return "Testing GraphQL with FastAPI. Hello!"

    @strawberry.field
    def askAQuestion(self, question: str) -> str:
        return retrieve_generate(question)


schema = strawberry.Schema(Query)

app = FastAPI(title="FastAPI GraphQL Hello")
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/v1/graphql")
