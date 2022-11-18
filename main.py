from fastapi import FastAPI

app = FastAPI()


# @app.get("/")
@app.get("/first")
async def root():
    return {"message": "Hello World"}  # 딕셔너리 형태
    # return "안녕하세요"

