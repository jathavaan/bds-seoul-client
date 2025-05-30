from typing import Union

from fastapi import FastAPI

from fastapi.responses import FileResponse


# 유저로부터 데이터를 받으려면 '모델'이라는 게 필요한데, 아래 import문이 그 모델을 불러오는 부분임. 아마 기본 모델인듯.
from pydantic import BaseModel


class Item(BaseModel):  # Item자리에 모델이름. 괄호 안에 BaseModel DI? 해줘야 함
    # 사용자가 입력할 수 있는 데이터의 변수 이름과 데이터 타입을 정의
    Game_ID: str


app = FastAPI()


@app.get("/")  # main page로 접속할 때 아래 정의된 함수를 실행함 (html 보여주거나, 특정 데이터를 보여주거나...)
def show_file():
    return FileResponse('index.html')
# get 자리엔 실제로 있는 함수들 중에서 필요한 기능들 호출
# / 자리엔 넣고 싶은 주소 (endpoint가 되는듯) /만 넣으면 메인 페이지 호출함.
    # 만약에 get("/")이랑 post("/")랑 둘 다 있으면 어떻게 됨?
    # 즉, endpoint가 동일하게 두 개 있으면 해당 url에 접속했을 때 어느 기능이 실행됨?
# return 다음에 원하는 아웃풋 작성. 특정 데이터 불러오는 등.. (get일 때 얘기겠지만)


@app.get("/recommendations")
def get_recommendations(steam_game_id: int):
    return {"game_id_received": steam_game_id}


@app.get("/game")
def data_input(data: Item):
    print(data)
    return '전송완료'


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
