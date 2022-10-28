# Maintainer:     Ryan Young
# Last Modified:  Oct 08, 2022
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import JsonModel

from .routers import users
from .routers import model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router( users.r, prefix='/users',
    tags=['Users'],
)
app.include_router( model.r, prefix='/model',
    tags=['Model'],
)

class Test(JsonModel):
    vals: list[list[float|str|None]]
    idxs: list[str]
    cols: list[str]


@app.get('/test/')
async def get_test_array():
    return {
        "vals": [[{"value": 1},{"value": 2},{"value": 3}],[{"value": 5},{"value": 6},{"value": 7}]],
        "idxs": ['P0','P1'],
        "cols": ['D0','D1','D2'],
    }



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

# TESTING ------------------------------
