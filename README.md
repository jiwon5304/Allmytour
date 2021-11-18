# Allmytour Makers
Allmytour 기업협업 프로젝트
  
## Members
|이름   |Github                   |Position|
|-------|-------------------------|--------------------|
|김태수 |[orosy](https://github.com/orosy)|  FE     |
|김영호 |[YOUNGHO8762](https://github.com/YOUNGHO8762) |   FE  |
|고준영 |[jay95ko](https://github.com/jay95ko)     | BE   |
|윤현묵 |[fall031-muk](https://github.com/fall031-muk)| BE   |
|박지원 |[jiwon5304](https://github.com/jiwon5304) | BE   |
|최현수 |[filola](https://github.com/filola) | BE |

## 프로젝트 내용
회사 측의 로컬 여행 가이드가 직접 여행 상품을 등록하는 웹 어플리케이션 개발 프로젝트
프로젝트 기능은 아래와 같습니다.
  - 회원가입/로그인 기능(비밀번호 찾기 포함)
  - 로그인을 진행한 사용자에 한하여 makers 지원하기 가능
  - 인적사항, 프로필 이미지, 증빙 서류 업로드 등 정보 입력
  - 정보 입력 중 임시저장 기능 가능
  - makers 제출 후 수정하기 기능 가능

</aside>

### [주요 고려 사항]
- 회원가입 관련 글
- makers 지원하기 도중 임시저장이 가능하도록 임시저장 table 따로 생성
- 이미지 및 파일 업로드를 위해 Django 내부 media 파일 전송 방식 이용

✔️ **API 상세설명**
---

- 회원가입/로그인 API
    - 
    - 
    - 
- makers 지원하기/임시저장 API
    - 로그인을 진행한 이후 지원하기 가능
    - 필수 입력사항과 추가 입력사항 구분
    - 프로필 이미지 파일, 신분증, 통장사본, 증빙서류 등 파일 업로드
    - 지원하기 작성 중 임시저장 가능
- makers 수정하기 API
    - 
    -   
  
## 구현 기능
### 회원가입/로그인
- 
- 
- 
- 

### maksers 지원하기/임시저장
- 필수 정보와 추가 정보를 입력받아 makers 지원하기(지원하기 시 필수 입력 값 미입력 시 지원할 수 없음)
- Django 내부 media 파일 전송 방식을 이용하여 프로필 이미지, 신분증, 통장사본, 증빙서류 등의 파일을 업로드
- 임시저장 table을 따로 작성하여 임시저장된 정보를 저장(필수 입력 값 미입력 시에도 임시저장 가능)

### maksers 수정하기
- 
- 
- 
- 
- 
- 

## 기술 스택
- Back-End : python, django, Mysql, 
- Tool     : Git, Gitlab, Slack, Flow

## 실행 방법(endpoint 호출방법)

### ENDPOINT

| Method | endpoint | Request Header | Request Body | Remark |
|:------:|-------------|-----|------|--------|
|POST|/user||name|회원가입 기능|
|POST|/makers/apply|access_token||makers 지원하기 기능(정보, 파일 등 업로드)|
|POST|/makers/draft|access_token||makers 임시저장 기능|
|POST|/makers/revise|access_token||makers 수정하기 기능|


## 폴더 구조
```
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── makers
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media
│   ├── bankbook
│   │   ├── 투어메이커스_1차.pdf
│   ├── evidence
│   │   └── wecode.jpeg
│   ├── idcard
│   │   └── wecode_AwIsSIl.jpeg
│   └── profile
│       ├── wecode.jpeg
├── my_settings.py
├── requirement.txt
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── decorator.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_user_auth_number.py
    │   ├── __init__.py
    ├── tests.py
    ├── urls.py
    └── views.py

```
