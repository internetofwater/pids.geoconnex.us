FROM python:3.9.13-slim

RUN \
    apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && git clone -b master https://github.com/internetofwater/geoconnex.us.git /geoconnex.us

RUN mkdir /build
COPY . /build/

WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r /build/requirements.txt

WORKDIR /build
CMD [ "python", "yourls_client.py", "--addr", "http://host.docker.internal:8082", "/build/namespaces/"]
