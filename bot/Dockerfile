FROM python:3.11-slim

WORKDIR /bot

RUN apt-get update && apt-get --yes upgrade

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /bot/docker-entrypoint.sh
RUN chmod +x /bot/wait-for-it.sh

ENTRYPOINT sh /bot/docker-entrypoint.sh

EXPOSE 8000