from typing import Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordRequestForm,
)
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
import uvicorn
import bcrypt

app = FastAPI()
security = HTTPBasic()
securiry2 = HTTPBearer()


# print('type: ', type(security)) # class instance


# HTTP Basic 인증
@app.get("/users/me")
def me(credentials: HTTPBasicCredentials = Depends(security)):
    #  http -v :8000/users/me Authorization:'Basic YWRtaW46MTIzNDEyMzQ='
    return {"username": credentials.username, "pwd": credentials.password}


###


## OAuth2 인증방식
HS256 = "HS256"
# `
# SECRET_KEY`는 *최소 32바이트* 문자열이면 됩니다.
# 다음과 같은 방법으로 생성할 수 있습니다.
# ```bash
# $ openssl rand -hex 32
#  또는 콘소렝서 파이썬 명령으로 암호화 문자를 생성할 수 있습니다
# $ python -c "import secrets;print(secrets.token_hex(32))"
# ```.
SECURITY_KEY = "e9f17f1273a60019da967cd0648bdf6fd06f216ce03864ade0b51b29fa273d75"
db = {
    "fastcompus": {
        "id": 1,
        "username": "fastcompus",
        "email": "fastcompus@email.com",
        "password": "$2b$12$kEsp4W6Vrm57c24ez4H1R.rdzYrXipAuSUZR.hxbqtYpjPLWbYtwS",
    },
}


class User(BaseModel):
    id: int
    username: str
    email: str


class UserPayload(User):
    exp: datetime


async def create_access_token(data: dict, exp: Optional[timedelta] = None):
    """Create access token"""
    expire = datetime.now() + (exp or timedelta(minutes=30))
    user_info = UserPayload(**data, exp=expire)
    # HS256 방식으로 유저 필드값으로 압호화 한다.
    return jwt.encode(user_info.dict(), SECURITY_KEY, algorithm=HS256)


@app.post("/login")
async def login_user(
    oauth_form: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> str:
    # print(oauth_form)
    user: dict = db.get(oauth_form.username)
    if not user:
        raise HTTPException(404, detail=f"NOT FOUND USER <{oauth_form.username}>")

    if bcrypt.checkpw(oauth_form.password.encode(), user.get("password").encode()):
        return await create_access_token(user, exp=timedelta(minutes=30))

    raise HTTPException(401, detail="패스워드 불일치!")


async def get_user(cred: HTTPAuthorizationCredentials = Depends(securiry2)):
    jwt_token = cred.credentials
    try:
        decoded_user = jwt.decode(jwt_token, SECURITY_KEY, HS256)
        # print(decoded_user) # {'id': 1, 'username': 'fastcompus', 'email': 'fastcompus@email.com', 'exp': 1639502469}
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired over!")  # 시간 만료 토큰
    except JWTClaimsError as error:
        raise HTTPException(400, str(error))
    except JWTError:
        raise HTTPException(401, "Invalid signature")  # 잘못된 토큰값 입력

    user_info = User(**decoded_user)
    return db.get(user_info.username)


@app.get("/me", response_model=User)
def get_current_user(user: dict = Depends(get_user)):
    return user


if __name__ == "__main__":
    uvicorn.run("10_authrize:app", reload=True)

    # jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJmYXN0Y29tcHVzIiwiZW1haWwiOiJmYXN0Y29tcHVzQGVtYWlsLmNvbSIsImV4cCI6MTYzOTUwMjQ2OX0.cIyOwg4U8J2a3dHERgvc8Mry9xvxH5mrMhlyWs0IRBc"
    # jwt.io 로 가서 토큰을 풀어보면 유저정보를 알수 있다.
