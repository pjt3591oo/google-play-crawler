# **구글 플레이 크롤러**

해당 프로젝트는 2개의 실행 파일로 구성되어 있습니다.

## 1. 사용 라이브러리

```
- selenium : 로그인을 및 각종 이벤트처리를 위해 사용
- sqlalchemy : 디비 orm라이브러리, 하지만 디비로 저장은 하지 않았다. 디비의 특성상 255자가 넘어가면 짤리는 현상 때문에 일단은 텍스트로 저장을 한다
```

## 2. 환경설정 셋팅

##### 2-1. 계정설정

`config/ACCOUNT_config.py`
```
EMAIL = ''
PASSWORD = ''
```

email과 password 설정을 해줍니다.
구글 플레이에서 특정 카테고리는 로그인을 해야 접속이 가능

##### 2-2. db설정
`config/DB_config.py`
```json
db_connection_info={
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "test",
    "charset": "utf8",
    "uri": 'mysql://root@localhost/test?charset=utf8'
}
```

본인이 사용하고 있는 디비 설정
 
##### 2-3. url설정

`URL_config.py`

```
LOGIN_URL = "https://accounts.google.com/ServiceLogin?hl=ko&passive=true&continue=https://www.google.co.kr/#identifier"
TOP_URL = "https://play.google.com/store"
BASE_URL = "https://play.google.com"
```
 
해당 파일설정은 건드리지 않는다 
 
## 3. 실행

##### 3-1. 카테고리 수집

```bash
$ python3 category_save.py
```

댓글을 수집 하기 앞서 모든 카테고리를 수집한다
현재 텍스트 파일로 저장을 한다.(`googleplay_category_link.txt`)

##### 3-2.댓글수집
```bash
$ python3 commend_collect.py
```
`googleplay_category_link.txt`에서 카테고리를 읽어서 모든 앱을 탐색하여 댓글을 수집한다.
간혹가다 한글이 깨지는 현상발생(이 부분은 엄청 많이 발생하는 경우는 아님)


> 생각보다 카테고리 갯수도 그렇고 댓글 갯수가 상당히 많았음. 카테고리는 약 400개, 댓글은 12시간 정도 작동하여 50Mb정도 수집(완전히 다 긁지는 못했다). 