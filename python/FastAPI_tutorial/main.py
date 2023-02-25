from enum import Enum
from turtle import st
from typing import Any, Dict, List, Set, Union

import fastapi
from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, EmailStr, Field, HttpUrl

app = FastAPI()


@app.post("/items/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
