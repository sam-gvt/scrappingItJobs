

FROM python:3.12-alpine3.20
LABEL maintainer="sam.grandvincent.developer@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
	/py/bin/pip install --upgrade pip && \
	apk add --update --no-cache postgresql-client && \
	apk add --update --no-cache --virtual .tmp-build-deps \
		build-base postgresql-dev musl-dev linux-headers && \
	apk add bash chromium chromium-chromedriver && \
	/py/bin/pip install -r /tmp/requirements.txt && \
	if [ $DEV = "true" ]; \
		then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
	fi && \
	rm -rf /tmp && mkdir /tmp && chmod 1777 /tmp && \
	apk del .tmp-build-deps && \
	adduser \
		--disabled-password \
		--no-create-home \
		sam-user && \
	chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER sam-user

CMD ["run.sh"]


