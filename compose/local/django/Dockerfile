FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update \
  # dependencies for building Python packages
  && apk add --no-cache build-base \
  # psycopg2 dependencies
  && apk add --no-cache postgresql-dev \
  # Pillow dependencies
  && apk add --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev \
    tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev \
  # Translations dependencies
  && apk add --no-cache gettext \
  # Bash shell
  && apk add --no-cache bash

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start



WORKDIR /app

ENTRYPOINT ["/entrypoint"]