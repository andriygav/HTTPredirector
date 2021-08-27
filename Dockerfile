FROM python:3.8.9-slim

ENV PORT 80
ENV THREADS 4
ENV PYTHONPATH /app/

# flask requirements
COPY ./flask/requirements.txt /tmp/requirements.txt
RUN cat /tmp/requirements.txt | xargs --no-run-if-empty -l pip install \
     && rm -rf /tmp/* /root/.cache/*

COPY ./flask /app

WORKDIR /app/

RUN chmod  777 -R /app 

CMD ["sh", "flask.sh", "/config/config.cfg", "/config/http_proxy.yaml"]

