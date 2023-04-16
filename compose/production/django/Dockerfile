FROM python:3.10-slim-buster

LABEL maintainer="RealEstateSearch-Production"

ENV PYTHONUNBUFFERED 1
# for loging
RUN mkdir /app/logs && touch /app/logs/celeryInfo.log

RUN pip install poetry==1.3.2
WORKDIR /app

# Install poetry
COPY ./RealEstateSearch/poetry.lock /app/
COPY ./RealEstateSearch/pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN chmod +x /app/logs/celeryInfo.log
RUN poetry install

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential netcat \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

RUN mkdir /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles

# copy project code
COPY /RealEstateSearch .

RUN chown -R django:django /app

USER django

ENTRYPOINT ["/entrypoint"]