FROM python:3.11-alpine as builder
RUN apk update && \
    apk add --no-cache --virtual .build-deps build-base && \
    python3.11 -m venv /venv
COPY ./requirements.txt /requirements.txt
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

FROM python:3.11-alpine
RUN apk update && apk add --no-cache ffmpeg
COPY --from=builder /venv /venv
CMD ["/venv/bin/python3.11", "/app/main.py"]