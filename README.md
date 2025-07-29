
## Pyenv
> 프로젝트 별 파이썬 버전을 관리하기 좋음
 
```sh
pyenv install --list # 설치 가능한 목록
```

```sh
pyenv install 3.12.3 # 해당 버전 설치
```

```sh
pyenv local 3.12.3 # 해당 디렉토리 파이썬 버전 설정
pyenv global 3.12.3 # 전역 파이썬 버전 설정
```



## Poetry
> node의 package.json과 같이 모듈 버전 관리에 용이 한듯

```shell
python -m pip install --user pipx
python -m pipx ensurepath
pipx install poetry
poetry env use 3.11
poetry env remove python
poetry shell
```

```sh
poetry env info
```

```sh
poetry env use /Users/kimzerovirus/.pyenv/versions/3.12.3/bin/python # pyenv 사용시 다음과 같은 경로이다.
```

```sh
poetry env list
```

```sh
poetry env remove [list에서 찾은 이름]
```

```shell
poetry shell
poetry install
poetry add
```

## Fast API
서버 실행
```shell
uvicorn main:app --reload --port 8080
```


api docs
```shell
http://localhost:8000/docs
```

```shell
### ORM Library ###
poetry add sqlalchemy
```

sqlite는 파이썬 기본 패키지에 포함되어 있음

## 모델을 이용하여 테이블 자동 생성
SQLAlchemy의 alembic을 이용해 데이터베이스 테이블을 생성할 수 있음
```shell
poetry add alembic
```

alembic 초기화
```shell

alembic init migrations
```
alembic.ini 파일이 생성된다. url 주소를 설정한다.
<br/>
```ini
sqlalchemy.url = sqlite:///./myapi.db
```

`migrations/env.py`에 database metadata를 설정한다. 
```python
import database
...
target_metadata = database.Base.metadata,
```

리비전 파일 생성
```sh
alembic revision --autogenerate -m "revision message"
alembic upgrade head
```
위 과정을 통해 데이터베이스에 모델에서 정의한 테이블이 생성된다.
이러한 마이그레이션 리비전들은 `alembic_version`이라는 테이블에 기록된다.
버전 지우고 다시 할거면 `DROP TABLE alembic_version;` sql실행해서 버전 지우고 다시 하면 됨

```python
import models
from database import engine
models.Base.metadata.create_all(bind=engine)
```
다음과 같은 코드를 main.py에 작성하면 자동생성이 가능하나 테이블이 존재하지 않을 경우에만 생성한다.
이 후 변경은 감지하지 못하는듯

## DI
https://fastapi.tiangolo.com/tutorial/dependencies/

> fastapi가 제공하는 방식이 있고, dependency-injector를 활용하는 방법이 있음

fastapi는 Depends 함수를 이용해 의존성을 주입한다.
`dependency-injector` 를 이용하면 IoC(제어의 역전) 컨테이너 스타일의 클래스 기반 DI를 지원해서, 더 명시적이고 구조화된 방식으로 의존성을 주입할 수 있음
~~근데 이렇게 사용할거면 스프링이 훨 낫지 싶음~~

## pydantic
EmailStr 타입은 타입선언만으로 이메일 형식을 검증할 수 있다. 다만, 추가 패키지를 필요로 한다.
```shell
poetry add "pydantic[email]"
```

## fastapi 비동기
파이썬의 asyncio 패키지를 기반으로함.
async, await 이용

## pydantic_settings
환경 변수 관리
dotenv
```shell
poetry add python-dotenv
poetry add pydantic-settings
```

## jwt
```shell
poetry add "python-jose[cryptography]" python-multipart
```
form-data를 다루기 위한 python-multipart 라이브러리

## fastapi middleware
```python
from fastapi import FastAPI, Request

@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"Request path: {request.url.path}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response
```
스프링의 filter나 interceptor 같은 역할을 하는듯, 실행 시점은 요청 전후

## test
```shell
poetry add pytest pytest-mock freezegun
```
datetime 모듈을 직접 모킹해도 되지만 freezegun의 `@freeze_time` 테커레이터를 이용하면 항상 일정한 시각을 손 쉽게 얻을 수 있음 
```python
@freeze_time("2025-01-01")
```