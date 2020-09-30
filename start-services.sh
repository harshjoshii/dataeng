#!/bin/bash

echo -ne "Creating files and variables ..."
mkdir -p log && \
touch log/start-services.log && \
export DOCKER_CLIENT_TIMEOUT=120 && \
export COMPOSE_HTTP_TIMEOUT=120 && \
echo  -e "\\rCreating files and variables ... \e[32mdone\e[0m" || \
echo  -e "\\rCreating files and variables ... \e[31merror\e[0m"


echo -ne "Starting services ..." && \
docker-compose -f docker-compose-start-services.yml up -d &>> log/start-services.log && \
echo  -e "\\rStarting services ... \e[32mdone\e[0m" || \
echo  -e "\\rStarting services ... \e[31merror\e[0m"

exit 0
