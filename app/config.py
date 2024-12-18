from sqlmodel import  create_engine,SQLModel
import os 
from dotenv import load_dotenv
load_dotenv()

# connection string

connection_string = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(connection_string)

# when session start its create tables

def create_tables():
    SQLModel.metadata.create_all(engine)