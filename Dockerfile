FROM python:3.11

COPY ./app /event_manager/app
COPY requirements.txt manage.py /event_manager/

WORKDIR /event_manager/

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
