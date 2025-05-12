FROM python:3.11.12-alpine3.20

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --upgrade --no-cache postgresql-client && \
    apk add --update --upgrade --no-cache --virtual .tmp  \
    build-base postgresql-dev

RUN /py/bin/pip install -r /requirements.txt && apk del .tmp

COPY ./backend /backend
WORKDIR /backend

ENV PATH="/py/bin:$PATH"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
