from typing import Optional, Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

users = {
    1: {"name": 'Fast'},
    2: {"name": 'Park'},
    3: {"name": 'Jojo'},
}


# 예외처리
# 1) HttpException 예외를 던진다.
@app.get('/users/{user_id}')
async def read_user_by(user_id: int):
    if user_id in users.keys():
        return users.get(user_id)

    raise HTTPException(404, detail=f"<User: {user_id}> is not found!")


# 2) 사용자 정의 예외 클래스 정의
class NotFoundException(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    def __str__(self):
        return f'<{self.name}> is occurred. code: <{self.code}>'


# fastapi exception_handler 추가
# 이 예외핸들러가 없으면 서버응답이 responseBody Internal Server Error임..
@app.exception_handler(NotFoundException)
async def some_error_handler(request: Request, e: NotFoundException):
    return JSONResponse(
        content={"message": f'error => {e.name}'},
        status_code=e.code
    )


# 사용자정의로 예외던지면 스웨거 서버응답 responseBody Internal Server Error 나옴..
# 좋은 방법은 아니다.
@app.get('/error/{user_id}')
async def throw_some_error(user_id: int):
    if user_id in users.keys():
        return users.get(user_id)

    raise NotFoundException(f'user <{user_id}> not found.', 404)


class SomeFastException(HTTPException):
    def __init__(
            self,
            status_code: int,
            detail: str,
            headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code, detail, headers)


# 3) fastapi.HTTPException 확장
@app.get('/throws')
async def throw_http_error():
    raise SomeFastException(500, 'some fst api exception')


if __name__ == '__main__':
    uvicorn.run('08_exception_handle:app', reload=True)
    # uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
