from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai
import os
from dotenv import load_dotenv
host = os.getenv("HOST")
port = os.getenv("PORT")
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(model = "gemini-pro")
output_parser = StrOutputParser()
embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
