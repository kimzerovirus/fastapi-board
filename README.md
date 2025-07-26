
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

## Fast API

api docs
```shell
http://localhost:8000/docs
```

```shell
### ORM Library ###
pip install sqlalchemy
```

sqlite는 파이썬 기본 패키지에 포함되어 있음

## 모델을 이용하여 테이블 자동 생성
SQLAlchemy의 alembic을 이용해 데이터베이스 테이블을 생성할 수 있음
```shell
pip install alembic
```

alembic 초기화
```shell

alembic init migrations
```
alembic.ini 파일이 생성된다.
<br/>
리비전 파일 생성
```sh
alembic revision --autogenerate
alembic upgrade head
```
위 과정을 통해 데이터베이스에 모델에서 정의한 테이블이 생성된다.

```python
import models
from database import engine
models.Base.metadata.create_all(bind=engine)
```
다음과 같은 코드를 main.py에 작성하면 자동생성이 가능하나 테이블이 존재하지 않을 경우에만 생성한다.
이 후 변경은 감지하지 못하는듯

## DI
https://fastapi.tiangolo.com/tutorial/dependencies/
