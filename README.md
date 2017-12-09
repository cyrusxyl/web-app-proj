# web-app-proj
## Cyrus Xiyuan Liu (xiyuanl1)

### Introduction
In this web2.0 project I tried to create a Steam like game review website (extremely simplified of course).

I use django with postgresql back-end.

### Requirements
`Postgresql`  
`Python 2.7`  
`django`  
`django-filter`  
`django-updown`

### Setup
First, postgresql has to be installed. I worked on a MacOSX computer and installed mine with homebrew.

Then, in the python enviorment install `django`, `django-filter`, and `django-updown` packages. I installed mine via `pip install`

Setup database accordingly in `settings.py`.

`python manage makemigrations mygames`
`python manage migrate`
`python manage runserver`

By default I use `localhost` as my hostname. Open `localhost:8000` should start the web app.
