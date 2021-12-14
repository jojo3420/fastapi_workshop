import time
from typing import IO
from tempfile import NamedTemporaryFile

import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/file/size")
def get_file(file: bytes = File(...)):
    # bytes 타입을 바이트 스트럼 으로 받기
    print(type(file))
    return {"file_size": len(file)}


@app.post("/file/info")
async def echo_file_info(file: UploadFile = File(...)):
    # await file.write()
    file_like_obj = file.file
    content = await file.read()
    # print(content)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }


async def store_file(file: IO):
    """store file to local storage"""
    # time.sleep(3)
    with NamedTemporaryFile("wb", delete=False) as temp_file:
        temp_file.write(file.read())
        return temp_file.name


@app.post("/file/save")
async def save_file(file: UploadFile = File(...)):
    for i in range(5):
        print(i)
    # print('-' * 100)
    path = await store_file(file.file)
    print(path)
    for j in range(6, 10):
        print(j)
    # print('-' * 100)

    return {"file_path": path}


if __name__ == "__main__":
    uvicorn.run("07_file_save:app", reload=True)
