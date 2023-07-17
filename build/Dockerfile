FROM python:3.9.13-slim

RUN mkdir /build
COPY . /build/

WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r /build/requirements.txt

WORKDIR /build
CMD [ "python", "yourls_client.py", "--addr", "http://host.docker.internal:8082", "/build/namespaces/"]
