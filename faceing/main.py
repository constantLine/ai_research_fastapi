from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import  HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("processing/", response_class=HTMLResponse)
async def check_video(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request_body": request.body}
    )


@app.post("processing/video/{section}/cancel")
async def set_video(sectinon: int):
   pass


