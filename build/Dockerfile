FROM ubuntu:20.04 AS ZIP

ADD https://github.com/internetofwater/geoconnex.us/archive/refs/heads/master.zip /master.zip

RUN apt-get update \
    && apt-get install unzip \
    && unzip -qq ./master.zip

FROM python

RUN mkdir /build
COPY . /build/

WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r /build/requirements.txt

COPY --from=ZIP /geoconnex.us-master/namespaces/ /build/namespaces/

WORKDIR /build
CMD [ "python", "yourls_client.py", "--addr", "http://host.docker.internal:8082", "/build/namespaces/"]
