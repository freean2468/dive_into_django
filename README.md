# dive_into_django

장고 첫걸음

https://docs.docker.com/samples/django/ 을 참고해 Dockerizing.

# 실행 명령어

1. sudo docker-compose run web django-admin startproject composeexample.

2. docker-compose up

<!-- web service 컨테이너 접속 -->

3. docker exec -it dive_into_django_web_1 /bin/bash

4. apt-get update && apt-get upgrade

<!-- python manage.py dbshell 실행에 필요 -->

5. apt-get install postgresql postgresql-contrib

# 장고 핵심 개념

A Django app is a self-contained chunk of a larger project that focuses on a discrete portion of the whole. For example, a web project may contain a blogging app, a users app, a newsletter app, and more.
You tell Django what structure you want the database to have, and Django takes care of translating your Python instructions to SQL queries to be executed on your chosen database. While you can still write SQL if needed, you don’t have to: you simply define your data models in Python, and Django takes care of the rest.

<!-- 앱 생성 -->

1. python3 manage.py startapp users

2. 모델 생성

3. settings.py 에 생성한 앱을 추가

4. python manage.py makemigrations
<!-- 4. python manage.py makemigrations --empty --name users users -->

5. python manage.py migrate users
