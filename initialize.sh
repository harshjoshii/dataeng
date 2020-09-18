#!/bin/bash
echo "Initialization started"
echo "It takes longer if it is a very first run. Please wait for few minutes! "

echo -ne "Creating Docker volumes ..."
docker volume create mysql &> /dev/null && \
docker volume create airflow &> /dev/null && \
echo  -e "\\rCreating Docker volumes ... \e[32mdone\e[0m" && \
echo -ne "\\rInitializing sequential executor ..."
docker-compose -f docker-compose-initialize.yml up -d &> /dev/null

for i in {1..30}
do
    if [ "$(docker ps -aq -f status=exited -f name=airflow-init)" ]; then
        docker-compose -f docker-compose-initialize.yml down &> /dev/null
        echo -e "\\rInitializing sequential executor ... \e[32mdone\e[0m"
        break
    fi
    sleep 10s
done

echo -n "Changing executor to local executor ..."
docker run --rm --name access-volume -v airflow:/airflow ubuntuvim sed -i 's/.*executor =.*/executor = LocalExecutor/' /airflow/airflow.cfg && \
docker run --rm --name access-volume -v airflow:/airflow ubuntuvim sed -i 's/.*sql_alchemy_conn = .*/sql_alchemy_conn = mysql+mysqldb:\/\/airflow:airflow@mysql:3306\/airflow_mdb/' /airflow/airflow.cfg && \
echo -e "\\rChanging executor to local executor ... \e[32mdone\e[0m"

echo -ne "\\rInitializing local executor ..."
docker-compose -f docker-compose-initialize.yml up -d &> /dev/null

for i in {1..50}
do    
    if [ "$(docker ps -aq -f status=exited -f name=airflow-init)" ]; then
        docker-compose -f docker-compose-initialize.yml down &> /dev/null
        echo -e "\\rInitializing local executor ... \e[32mdone\e[0m"
        break
    fi
    sleep 10s
done

echo "Initialization complete"

exit 0
