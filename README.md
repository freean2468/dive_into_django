# dive_into_django

## 장고 첫걸음

django, DRF, memcached, postgresql 사용해 간단히 개발해 본 프로젝트

<!-- https://docs.docker.com/samples/django/ 을 참고해 Dockerizing. -->

<!-- https://blog.logrocket.com/dockerizing-django-app/ -->

## 실행 명령어

<!-- 1. sudo docker-compose run web django-admin startproject root. -->
개발 환경은 모두 docker 컨테이너화

```bash
# 프로젝트 최상위 폴더에서
docker-compose up
```

<!-- web service 컨테이너 접속 -->

<!-- 2. docker exec -it dive_into_django_web_1 /bin/bash -->

<!-- # 개발 환경 셋팅

1. 프로젝트가 컨테이너 내부에 있기 때문에 VS Code의 Remote-Containers Extension을 활용해 개발한다.

2. Palette => Remote-Containers: Open Folder in Container => start from Dockerfile -->

<!-- python manage.py dbshell 실행에 필요 -->
<!-- 3. apt-get install postgresql postgresql-contrib -->

## API 문서

http://localhost:8000/docs/#/

![api_doc](https://i.imgur.com/daIxKZa.png)


## 서비스 흐름도

![api_flow_1](https://i.imgur.com/zT3FIae.png)


![api_flow_2](https://i.imgur.com/vXB6ABl.png)


![api_flow_3](https://i.imgur.com/YyEeufz.png)

## 장고 핵심 개념

<!-- https://blog.logrocket.com/making-django-migrations-python/ -->

A Django app is a self-contained chunk of a larger project that focuses on a discrete portion of the whole. For example, a web project may contain a blogging app, a users app, a newsletter app, and more.
You tell Django what structure you want the database to have, and Django takes care of translating your Python instructions to SQL queries to be executed on your chosen database. While you can still write SQL if needed, you don’t have to: you simply define your data models in Python, and Django takes care of the rest.

<!-- 앱 생성 -->

<!-- 1. python3 manage.py startapp users

2. 모델 생성

3. settings.py 에 생성한 앱을 추가 -->

```bash
# 컨테이너 내부로 접속
docker exec -it dive_into_django_web_1 /bin/bash

# DB migration
python manage.py makemigrations
python manage.py migrate
```
<!-- 4. python manage.py makemigrations --empty --name users users -->

<!-- python manage.py check -->
<!-- python manage.py sqlmigrate -->
<!-- python3 manage.py showmigrations -->

## DRF (Django REST framework)

<!-- https://blog.logrocket.com/using-react-django-create-app-tutorial/ -->

A view is the initial entrypoint of a request made upon a specific endpoint served by a URL.

This is all mapped by the Django REST framework once we connect the function itself to the endpoint.

<!-- # Admin -->

<!-- python manage.py createsuperuser -->

## Auth

django 기본 인증 시스템과 DRF의 내장 인증 시스템을 사용해 장고 환경에 적응해보자.

## TDD

8개의 API에 대해 50가지 테스트 케이스를 작성.
테스트는 많으면 많을수록 좋다. 아직 더 작성할 테스트 케이스가 남아 있다.
이후에 cache의 timeout 환경까지 재현해 테스트해보면 좋겠다.

## Cache

처음에는 redis를 고려했으나, 장고에서 native하게 지원하는 건 memcached라서 Memcached 사용.

## Schema

https://www.django-rest-framework.org/api-guide/schemas/

https://djangoadventures.com/coreapi-vs-openapi/

drf-yasg보다 drf-spectacular가 더 업데이트가 잘 되고, OpenAPI 3.0까지 지원해준다.

```bash
./manage.py spectacular --file schema.yml
```

<!-- # db 초기화

1. in psql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

2. numbering된 migrations를 모두 삭제하고 
python manage.py makemigrations
python manage.py migrate --run-syncdb -->

## Code Quality 
- https://realpython.com/python-code-quality/
- VS code linter setting : https://code.visualstudio.com/docs/python/linting
  - PEP8과 PEP 257 linter를 포함한 pylama가 좋겠다.

- Type Hinting 추가해야 한다.
- 컨테이너로 가상화를 하니 poetry를 사용할 동기가 부족해지는 거 같다.

## 인증

1. 인증을 별도의 Microservice로 빼고 싶다. DRY : https://medium.com/@akiva10b/microservice-infrastructure-with-django-8f985e86a057


## deploy

배포도 추후 도전


## 보완해야할 점

1. 현재 인증시스템으론 멀티 디바이스 로그인과 로그아웃 기능을 지원하지 못한다.
최소한 knox로 업그레이드하거나 jwt기반의 인증시스템을 별도로 만들 필요가 있다.

2. django에서 기본적으로 제공해주는 orm에서 만든 db 구조 및 해당 시스템이 어떻게 작동하는지 아직 이해가 부족하다.

3. 비동기 부분이 없다. 본인 스스로가 python 환경에서의 비동기 시스템이 어떻게 작동하는지에 대한 스터디가 더 필요하다.