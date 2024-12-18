from langchain_google_genai import ChatGoogleGenerativeAI
import os 

from dotenv import load_dotenv
load_dotenv()


llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Specify the model to use
    api_key=os.getenv('GEMINI_API_KEY'),     # Provide the Google API key for authentication
)



# llm_with_node = llm.bind_tools(tools)