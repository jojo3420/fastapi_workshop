import time
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'localhost',
    'localhost:8000'
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'OPTIONS'],  # 실제로 안먹히는데??
    allow_headers=['*']
)


@app.get('/')
def home():
    # http -v GET :8000/
    print('home')
    return {'msg': 'hello world'}


@app.post('/foo')
def not_allow_post():
    # POST 요청이 되네?? 뭐지??
    # http POST :8000/foo
    time.sleep(1)
    print('now_allow_post')
    return {
        'foo': 'A'
    }


# 미들웨어 만들기
@app.middleware('http')
async def process_time_mw(request: Request, call_next):
    method = request.method
    print(f'method: {method}')
    start_tm = time.time()
    response = await call_next(request)
    end_tm = time.time() - start_tm
    response.headers['X-Process-Time'] = str(end_tm)
    return response


if __name__ == '__main__':
    # 프리플라이트(Preflight reuqest) 요청 으로 허용가능한 요청 확인
    # http -v OPTIONS :8000 Origin:http://localhost Access-Control-Request-Method:GET

    # 실제로는 POST, origins 안먹힘..
    #  http -v POST :8000/foo Origin:http//www.naver.com Access-Control-Rquest-Method:GET

    uvicorn.run('12_middleware:app', reload=True)
