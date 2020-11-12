
#  Create a data pipeline architecture using docker-compose yaml file.
#  Intially architecture comprise of following services:
#  1. Airflow
#  2. MySql

Goal: To create a simple pipeline using airflow which should copy the file from a web location and place it in the local folder.

Airflow Service
- Must have a bind mount for airflow home. So that dags can be modified and airflow can be configured from the local folder.
- Must be able to communicate to the MySQL server to work with LocalExecutor
- Must be able to expose port 8080 to access the airflow web ui

MySQL Service
- On new image creation it must have a database named `airflow`
- It also must have a new user name and password as `airflow` for the airflow service to communicate


#  Create a dag for a pipeline to copy the file from the web location to the destination

Goal: To create the initial version of the pipeline where ingestion of the data will take place

List of Dags
- ingest-school-demo-student-demographics
- ingest-public-school-enrollment
- ingest-private-school-contact

- These dags must use the local executor to ingest these files from the following location to the local repository
- Once these files are copied. The data must be imported to the mysql server in the tables. 
- After the data is imported, airflow must send the email to the user on the status of the ingestion.
