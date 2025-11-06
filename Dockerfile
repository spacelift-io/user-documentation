FROM python:3.13.8-alpine
WORKDIR /docs

RUN apk update && apk add --no-cache git

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
