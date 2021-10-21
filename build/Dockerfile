FROM python

ENV YOURLS_DB_PASS=${YOURLS_DB_PASS}

RUN mkdir /build
COPY . /build/

WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r /build/requirements.txt

WORKDIR /build
CMD [ "python", "yourls_client.py", "--addr", "http://host.docker.internal:8082", "/build/namespaces/"]
