from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
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
