FROM python:3.9-alpine3.13
LABEL maintainer="RealEstateSearch-AWS-Cloud"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./RealEstateSearch /RealEstateSearch
COPY ./scripts /scripts
COPY ./.env.sample /.env.sample

WORKDIR /RealEstateSearch
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home RealEstateSearch && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R RealEstateSearch:RealEstateSearch /vol && \
    chmod -R 755 /vol && \
    chmod -R 755 /.env.sample && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER RealEstateSearch

CMD ["run.sh"]