FROM python:3.12

ENV PYTHONUNBUFFERED 1


WORKDIR /app

RUN git init


COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

ENV PORT 8000


CMD python manage.py migrate && uwsgi --ini deploy/uwsgi.ini --http-socket :$PORT --static-map /static=/app/static --callable kitten_exhibition.wsgi:application

