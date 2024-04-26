from typing import Union

from fastapi import FastAPI, Request, UploadFile, File,  Depends, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from utils import *

from models import crud, models, schemas
from models.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/processing/", response_class=HTMLResponse)
async def check_video(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request_body": request.headers}
    )


@app.post("/processing/")
async def upload_video(file: UploadFile = File(...)):
    content_path = "media/static.jpg"
    await write_content(content=file, content_path=content_path)
    return {"filename": file.filename}


@app.post("/processing/video/{section}/cancel")
async def set_video(sectinon: int):
   pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/news/", response_model=schemas.News)
def create_news_for_user(
    user_id: int, news: schemas.NewsCreate, db: Session = Depends(get_db)
):
    return crud.create_user_news(db=db, news=news, user_id=user_id)


@app.get("/news/", response_model=list[schemas.News])
def read_news(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    news = crud.get_news(db, skip=skip, limit=limit)
    return news




