from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ To-Do Database Model
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Pydantic Model for API Requests & Responses
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoResponse(TodoCreate):  # Inherits from TodoCreate but adds `id`
    id: int

# ✅ Create a To-Do
@app.post("/todos/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoDB(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# ✅ Get All To-Dos (Now includes ID)
@app.get("/todos/", response_model=List[TodoResponse])
async def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoDB).all()

# ✅ Get a Single To-Do (Now includes ID)
@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return todo

# ✅ Update a To-Do
@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, updated_todo: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="To-Do not found")

    for key, value in updated_todo.dict().items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

# ✅ Delete a To-Do
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="To-Do not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "To-Do deleted successfully"}
