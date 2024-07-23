
from fastapi import FastAPI, Depends
from typing import Annotated
from app import settings
from contextlib import asynccontextmanager
from sqlmodel import SQLModel,Field,create_engine, Session, select

# database table
class todos(SQLModel, table=True):
    id:int| None = Field(default= None, primary_key= True)
    title: str = "Create Todo API"
   
    


# connection with databalise
connection_string: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string)


def create_db_tables():
    print("db_tables")
    SQLModel.metadata.create_all(engine)
    
    
@asynccontextmanager
async def lifespan(todo: FastAPI):
    print("server start uo")
    create_db_tables()
    yield

# table data save ,get, update, delete

todo: FastAPI = FastAPI(lifespan= lifespan) 

@todo.get("/")
def hello():
    return {"hello":"mylady"}

def get_session():
    with Session(engine) as session:
        yield session

@todo.post("/todo")
def create_todo(todo_data:todos, session: Annotated[Session, Depends(get_session)]):
    session.add(todo_data)
    session.commit()
    session.refresh(todo_data)
    return todo_data
        
        
    # get all todos data
    
@todo.get("/todo")
def get_all_todos(new_concept: Annotated[Session, Depends(get_session)]):
    query = select(todos)
    all_todos = new_concept.exec(query).all()
    return all_todos



# dependency injection core concept
# from fastapi import FastAPI, Depends
# from typing import Annotated
# app = FastAPI()
 
# def greeter(myname: str):
#     print (" 1 greeter")
#     greeting = myname + " welcome"
#     return greeting
 
# @app.get("/")
# def name(myname: str , greet_msg :Annotated[str,Depends(greeter)]):
# #    full_name = myname + "juju"
#    print (" 2 name")
# #    greet_msg = greeter(myname)
#    return {greet_msg + "hi"}