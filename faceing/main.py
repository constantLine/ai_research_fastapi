from typing import Union

from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils import *


app = FastAPI()

templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


from fastapi import FastAPI

app = FastAPI()


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


