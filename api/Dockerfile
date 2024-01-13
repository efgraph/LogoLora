FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev

WORKDIR /api

RUN apt-get update && apt-get --yes upgrade

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install --upgrade pip

COPY . .

RUN chmod +x /api/docker-entrypoint.sh

ENTRYPOINT sh /api/docker-entrypoint.sh

EXPOSE 8000