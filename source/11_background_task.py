import time
from typing import Optional

import uvicorn
from fastapi import FastAPI, BackgroundTasks, status, Depends

app = FastAPI()


def file_write(message):
    # 오래 걸리는 작업 이라고 가정
    time.sleep(3)
    with open("log.txt", mode="a") as f:
        f.write(message)


#  http POST ''http://127.0.0.1:8000/task\?email\=jjjhhhvvv%40naver.com'\
@app.post("/task", status_code=status.HTTP_202_ACCEPTED)
def background_task_handle(email: str, background_task: BackgroundTasks):
    message = f"message sent: {email}\n"

    # background_task 에게 태스크를 주고 바로 응답한다.
    # 단점은 background가 미처리 되었거나 예외가 발생했을때 클라이언트 결과 전달 어려움.
    background_task.add_task(file_write, message)
    return {"msg": "Accepted Task"}


# 의존성 주입 방식으로 사용
def get_query(background_task: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_task.add_task(file_write, message)


# 핸들러 DI를 이용하여 응용도 가능.
# http POST ':8000/double/task?email=www%40naver.com&q=hello%20world'
@app.post("/double/task", status_code=status.HTTP_202_ACCEPTED)
def double_task(
    email: str,
    background_task: BackgroundTasks,
    q: str = Depends(get_query),  # 매개변수 ID에서 백그라운드 태스크 처리!
):
    message = f"message to {email}\n"
    background_task.add_task(file_write, message)
    return {"message": "Accepted task!"}


if __name__ == "__main__":
    uvicorn.run("11_background_task:app", reload=True)
