from app.crawler import discover_site_urls

import os
import warnings

warnings.filterwarnings(
    "ignore",
    message=".*LangChain uses pydantic v2 internally.*",
    category=DeprecationWarning,
)
# To let servers know who is calling them
os.environ["USER_AGENT"] = "my-rag-application/0.1 (contact: Leonard Eshun)"


from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.chat_models import init_chat_model


# Load variables from .env into os.environ
load_dotenv()

# Initialize the Gemini 2.5 model from Google GenAI for chat model
chat_model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# Initialize OpenAI embeddings for creating embeddings
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Initialize Pinecone vector store for storing and retrieving embeddings
index_name = "langchain-rag-3072-full"
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))


def setup_pinecone_with_external_data():
    print("Setting up Pinecone with external data...")
    pc.create_index(
        name=index_name,
        dimension=3072,  # embedding size for text-embedding-3-large
        metric="cosine",  # or "dotproduct"/"euclidean"
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

    index = pc.Index(name=index_name)
    vector_store = PineconeVectorStore(embedding=embeddings_model, index=index)

    # Get the URLs by crawling my personal website
    urls = discover_site_urls(
        "https://leonardeshun.com/",
        max_pages=15,
        include_subdomains=False,
        delay_seconds=0.5,
        allow_paths=None,
        deny_paths=["/admin", "/login"],
    )

    # Load and chunk contents of my website
    if not urls:
        print("No URLs found to crawl.")
        return

    for url in urls:
        loader = WebBaseLoader(url)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(docs)

        # Index chunks
        _ = vector_store.add_documents(documents=all_splits)


# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    index = pc.Index(name=index_name)
    vector_store = PineconeVectorStore(embedding=embeddings_model, index=index)
    retrieved_docs = vector_store.similarity_search(state["question"], k=20)
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = chat_model.invoke(messages)
    return {"answer": response.content}


def retrieve_generate(question: str) -> str:
    if not pc.has_index(index_name):
        setup_pinecone_with_external_data()
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    response = graph.invoke({"question": question})
    return response["answer"]


# Test the application with a sample question
if __name__ == "__main__":
    if not pc.has_index(index_name):
        setup_pinecone_with_external_data()
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    question = "What did Leonard do at virginia tech?"
    print(
        f"*********************** Answering the question - {question} ***********************"
    )
    response = graph.invoke({"question": question})
    print(response["answer"])
