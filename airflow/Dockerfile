
FROM apache/airflow

USER root

RUN sudo apt-get update && apt-get install -y --no-install-recommends wget gcc g++

ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN chown airflow /usr/local/bin/dockerize 

RUN sed -i '$ d' /entrypoint

RUN sed -i "\$a exec dockerize -wait tcp://mysql:3306 -timeout 300s -wait-retry-interval 10s airflow \"\${@}\"" /entrypoint

WORKDIR /opt/airflow

USER airflow

RUN pip install --user --upgrade pip  \
    && pip install --user python-csv hdfs xlrd3

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]



