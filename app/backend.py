import strawberry
from fastapi import FastAPI
from langchain_core.messages import AIMessage, HumanMessage
from strawberry.fastapi import GraphQLRouter

from .rag_application import retrieve_generate


@strawberry.input
class ChatMessageInput:
    role: str
    content: str


@strawberry.type
class Query:
    @strawberry.field
    def askAQuestion(
        self,
        question: str,
        chat_history: list[ChatMessageInput] | None = None,
    ) -> str:
        history = []
        if chat_history:
            for msg in chat_history:
                if msg.role == "human":
                    history.append(HumanMessage(content=msg.content))
                else:
                    history.append(AIMessage(content=msg.content))
        return retrieve_generate(question, history)


schema = strawberry.Schema(Query)

app = FastAPI(title="RAG Backend")
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/v1/graphql")
