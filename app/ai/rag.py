from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
# app/ai/data.txt
try:
    # load data using text loader
   loader = TextLoader("./app/ai/data.txt")
except Exception as e:  
    print("Error while loading file=", e)

# Load Data
# loader = TextLoader("./data.txt")
documents = loader.load()

prompt = hub.pull("hwchase17/openai-tools-agent")
# Split data into Chunks
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)
# Create Embaddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever()

# Create  as a Tool
info_retriever = create_retriever_tool(
    retriever,
    "skyassist_information_sender",
    "Searches information about skyassist(airline) from provided vector and return accurare as you can",
)
