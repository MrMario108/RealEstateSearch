FROM python:3.10.6

LABEL maintainer="RealEstateSearch-New-docker"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry==1.3.2
WORKDIR /app

# for loging
RUN mkdir /app/logs && touch /app/logs/celeryInfo.log


# Install poetry
COPY ./RealEstateSearch/poetry.lock /app/
COPY ./RealEstateSearch/pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN chmod +x /app/logs/celeryInfo.log
RUN poetry install


RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# Requirements are installed here to ensure they will be cached.
#COPY ./requirements.txt /requirements.txt
#RUN pip install -r /requirements.txt


COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower



ENTRYPOINT ["/entrypoint"]