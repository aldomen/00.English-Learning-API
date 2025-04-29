# this is the main script.
## uvicorn main:app --reload --port 3000

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, EnglishSpanish


app = FastAPI()
# set up the middleware 
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# setup the pydantic
## this is the information that comes from the APP for validations.
class WordsBase(BaseModel):
    english: str
    spanish: str

## this is the data for the database
class WordsModel(WordsBase):
    id: int
    date: str | None


# set up the db
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
Base.metadata.create_all(bind=engine)

# Endpoints
@app.post("/api/words", response_model=WordsModel)
async def create_words(words: WordsBase, db: db_dependency):
    db_words = EnglishSpanish(**words.model_dump())
    db.add(db_words)
    db.commit()
    db.refresh(db_words)
    return db_words

@app.get("/api/words", response_model=List[WordsModel])
async def get_words(db: db_dependency, skip: int = 0, limit: int = 10):
    words = db.query(EnglishSpanish).offset(skip).limit(limit).all()
    return words