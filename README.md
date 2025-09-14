# A RAG application using LangChain
## RAG Project Description
This project shows a LangGraph pipeline served via FastAPI + Strawberry GraphQL with vector search in Pinecone and displayed via a Flask frontend application.    
### A Screenshot of the Application
![A screenshot of the application](images/screenshot.png)
A screenshot of the application is shown above. The user enters a question in the text area and clicks the "Ask" button. The question is sent to the FastAPI backend which calls the function to start executing the steps of the LangGraph. The answer is returned through the same pipeline and displayed on the Flask Frontend application.     
<br>
The RAG application uses my personal website https://www.leonardomoroney.com/ as the source of information to answer questions. The website is crawled and the contents are stored in Pinecone for later retrieval.
<br>

### A Screenshot of the Description Card
![A screenshot of the application](images/screenshot2.png)
A screenshot of the description card is shown above. It describes the indexing and question-and-answer processes of the application.     
<br>

### The Indexing Process
![Abstract tech background](web/static/indexing.png)
A crawler crawls my website to get all the loadable links. Then the contents of the links are loaded and chunked for easier processing by the models. Embedding are created from the chunks and stored in Pinecone for later retrieval.

### Try asking
1. “What projects are on his website?”    
1. “What tools does he use for data engineering?”    

### The Question-and-Answer Process
![Abstract tech background](web/static/retrieval.png)
The question is entered into the Flask frontend application. It's sent to the FastAPI GraphQL backend which calls the function to start executing the steps of the LangGraph. An embedding is created from the question and a similarity search done in Pinecone to find semantically related text to the question.      
<br>
This is the context, and it is added to the question to create a prompt for Google's Gemini Flash chat model to generate the answers. The answer is returned through the same pipeline and displayed on the Flask Frontend application.     
<br>
This RAG application can be used for any website. Just change the website in the code on GitHub.