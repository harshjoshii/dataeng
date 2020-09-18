#!/bin/bash
mkdir -p log
touch log/start-services.log && \
echo -ne "Starting services ..." && \
docker-compose -f docker-compose-start-services.yml up -d &>> log/start-services.log && \
echo  -e "\\rStarting services ... \e[32mdone\e[0m"

exit 0
