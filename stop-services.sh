#!/bin/bash
mkdir -p log
touch log/stop-services.log && \
echo -ne "Stopping services ..." && \
docker-compose -f docker-compose-start-services.yml down &>> log/stop-services.log && \
echo  -e "\\rStopping services ... \e[32mdone\e[0m"

exit 0
