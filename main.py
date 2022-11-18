from fastapi import FastAPI
from pydantic import BaseModel

class Cat(BaseModel):
    name : str
    id: int = 0

app = FastAPI()


# @app.get("/")
# @app.get("/first")
@app.get("/first/{id}")  # 키 없이 / 구분
# async def root(id):
async def root(id: int):
    return {"message": "Hello World", "id": id}  # 딕셔너리 형태
    # return "안녕하세요"

@app.get("/second")  # 쿼리 매개변수
async def second(skip:int = 0, limit:int = 10):
    return {"skip":skip, "limit":limit}

@app.post("/cat")
async def cat(cat: Cat):  # cat 라는 함수 안에 cat 이라는 변수(?)
    # return ...  # ...: 생략할 때 / JS의 ...과 다르다. pass는 에러 발생
    return cat
