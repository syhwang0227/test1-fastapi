from databases import Database
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# 에러 처리
class ResponseDTO(BaseModel):
    code: int
    message: str
    data: object



class Cat(BaseModel):
    name : str
    id: int = 0

app = FastAPI()


origins = [
    "http://127.0.0.1:5500",  # 라이브서버는 5500 포트 사용
    # "*" 모든 포트 허용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # methods: get, post delete put
    allow_headers=["*"],  # 모든 헤더를 다 받겠다는 의미
)

database = Database("sqlite:///C:\programming\sqlite\hr")

# @app.get("/")
# @app.get("/first")
@app.get("/first/{id}")  # 키 없이 / 로 구분
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

@app.get("/error")
async def error():
    # if True:
    #     return JSONResponse(status_code=200, content={"message": "Item not found"})
    # else:    
    #     return JSONResponse(status_code=404, content={"message": "Item not found"})
    dto = ResponseDTO(
        code=0,
        message="페이지가 없습니다.",
        data=None
    )
    return JSONResponse(status_code=404, content=jsonable_encoder(dto))

@app.get("/error1")
async def error1():
    return HTTPException(status_code=404, detail={"message": "Item not found"})

@app.post("/files/")
async def check_file(
    uploadFile: UploadFile = File(), token: str = Form()
):
    return {
        "token": token,
        # "uploadFileSize": len(await upload_file.read()),
        "uploadFileName": uploadFile.filename,
        "uploadFileContentType": uploadFile.content_type,
    }

@app.get("/findall")  # 요청이 들어오면 아래 함수 실행
async def fetch_data():

    await database.connect()  # await: 연결할 때 까지 기다리겠다.

    query = "SELECT * FROM REGIONS"  # 실무에서는 *를 사용하지 말고 다 입력해야 한다.
    results = await database.fetch_all(query=query)  # fetch_all: 데이터를 모두 가져오겠다.

    await database.disconnect()  # disconnect: 연결 해제

    return results