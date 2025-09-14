# A RAG application using LangChain
## RAG Project Description
This project shows a LangGraph pipeline served with FastAPI + Strawberry GraphQL with vector search in Pinecone and displayed via a Flask frontend application.    
### A Screenshot of the Application
![A screenshot of the application](images/main_app.png)
A screenshot of the application is shown above. The user enters a question in the text area and clicks the "Ask" button. The question is sent to the FastAPI backend which calls the function to start executing the steps of the LangGraph. The answer is returned through the same pipeline and displayed on the Flask Frontend application.     
<br>
The RAG application uses my personal website https://www.leonardeshun.com/ as the source of information to answer questions. The website is crawled and the contents are stored in Pinecone for later retrieval.
<br>

### A Screenshot of the Description Card
![A screenshot of the application](images/description_card.png)
A screenshot of the description card is shown above. It describes the indexing and question-and-answer processes of the application.     
<br>

### The Indexing Process
![Abstract tech background](images/indexing.png)
A crawler crawls my website to get all the loadable links. Then the contents of the links are loaded and chunked for easier processing by the models. Embedding are created from the chunks and stored in Pinecone for later retrieval.

### Try asking
1. “What projects are on his website?”    
1. “What tools does he use for data engineering?”    

### The Question-and-Answer Process
![Abstract tech background](images/retrieval.png)
The question is entered into the Flask frontend application. It's sent to the FastAPI GraphQL backend which calls the function to start executing the steps of the LangGraph. An embedding is created from the question and a similarity search done in Pinecone to find semantically related text to the question.      
<br>
This is the context, and it is added to the question to create a prompt for Google's Gemini Flash chat model to generate the answers. The answer is returned through the same pipeline and displayed on the Flask Frontend application.     
<br>
This RAG application can be used for any website. Just change the website in the code on GitHub.

### Technologies Used
- LangChain
- LangGraph
- FastAPI
- Strawberry GraphQL
- Flask
- Pinecone
- Google Gemini Flash 2.5 model
- Python
- HTML/CSS/JavaScript
- OpenAI's text-embedding-3-large model

### To run the application
1. Clone the repository
1. Install the required packages using `pip install -r requirements.txt`
1. Set the required environment variables in a `.env` file:
   - GOOGLE_API_KEY=Your_Google_API_key
   - PINECONE_API_KEY=Your_Pinecone_API_key
   - OPENAI_API_KEY=Your_OpenAI_API_key
   - LANGSMITH_API_KEY=Your_Pinecone_environment
   - LANGSMITH_TRACING=true
1. Run the FastAPI backend using `uvicorn app.backend:app --host 0.0.0.0 --port 8000`
1. Run the Flask frontend using `python web/frontend_app.py`
1. Go to `http://localhost:5070` to access the application

### Deployment
I may deploy this application using Docker and hosted on a cloud platform using services like Google Cloud Run or AWS Fargate to run the Docker containers soon. Another option is to use a cloud compute service like Google Compute Engine or AWS EC2 to run the application directly on a virtual machine. However, the easiest option is to deploy it on th LangChain Hub. I'll decide soon.

### Why LangGraph?
The RAG application could have been done without LangGraph. However, I chose LangGraph to understand how it works and can be used in agentic AI designs, informing my design options in the future. It also has LangSmith, which traces all activites on the application and gives insight on what is going on. See the screenshot below of the tracing of the application on LangSmith.    
![LangSmith tracing of the application](images/langsmith.png)  
There are more benefits of using LangGraph when designing more complex agentic applications and state management is important.     

### Note
You'll need the necessary API keys and access to the services used in this project in your environment to run it.