#!/bin/bash
echo -ne "Creating files and variables ..."
mkdir -p log && \
touch log/start-services.log && \
export DOCKER_CLIENT_TIMEOUT=200 && \
export COMPOSE_HTTP_TIMEOUT=200 && \
echo  -e "\\rCreating files and variables ... \e[32mdone\e[0m" || \
echo  -e "\\rCreating files and variables ... \e[31merror\e[0m"

echo -ne "Stopping services ..." && \
docker-compose -f docker-compose-start-services.yml down &>> log/stop-services.log && \
echo  -e "\\rStopping services ... \e[32mdone\e[0m"

exit 0
