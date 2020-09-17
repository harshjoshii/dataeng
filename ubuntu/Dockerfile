FROM ubuntu

RUN apt-get update

RUN apt-get install -y   git && apt-get install -y vim

# Command to run the container 
# docker run -it --rm --name access-volumes -v airflow:/airflow ubuntuvim /bin/bash


# Shell Snippets

# To change executor to LocalExecutor
# sed -i 's/.*executor =.*/executor = LocalExecutor/' airflow.cfg

# To change sql alchemy conn for mysql
# sed -i 's/.*sql_alchemy_conn = .*/sql_alchemy_conn = mysql+mysqldb:\/\/airflow:airflow@mysql:3306\/airflow_mdb/' /opt/airflow/airflow.cfg 