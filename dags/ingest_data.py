import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from hdfs_lib import upload_to_hdfs

default_args = {
    'owner' : 'airflow',
    'start_date': dt.datetime(2020, 1, 1),
    'retries': 0
}


school_board_school_authority_contact_dlink = "https://data.ontario.ca/dataset/9831236f-6e01-447a-9e28-b9c6b3348631/resource/d35fba1d-54fc-4250-b97e-3134a62d4c3a/download/boards_schoolauthorities_september_2020_en.xlsx"
public_school_contact_info_dllink = "https://data.ontario.ca/dataset/fb3a7c18-90af-453e-bc0a-a76ecc471862/resource/523b98e0-c677-4ac4-b453-08e9727cb712/download/publicly_funded_schools_xlsx_september_2020_en.xlsx"
private_school_contact_info_dlink = "https://data.ontario.ca/dataset/7a049187-cf29-4ffe-9028-235b95c61fa3/resource/6545c5ec-a5ce-411c-8ad5-d66363da8891/download/private_schools_contact_information_september_2020_en.xlsx"
academic_year_dlink = "https://files.ontario.ca/opendata/enrolment_by_school_1718_en_supp.xlsx"
school_info_student_demographics_dlink = "https://data.ontario.ca/dataset/d85f68c5-fcb0-4b4d-aec5-3047db47dcd5/resource/602a5186-67f5-4faf-94f3-7c61ffc4719a/download/new_sif_data_table_2018_2019prelim_en_august.xlsx"

with DAG('ingest_data',
        default_args=default_args,
        schedule_interval='@daily',
        description='A simple dag to download open data files from ontario.ca ',
        catchup=False) as dag:

        # Download files to a shared volume
        download_school_board_school_authority_contact = BashOperator(task_id='download_school_board_school_authority_contact', bash_command='wget -O /shared-volume/ontario-school-data/' + school_board_school_authority_contact_dlink.split("/")[-1] + ' ' + school_board_school_authority_contact_dlink)
        download_public_school_contact_info = BashOperator(task_id='download_public_school_contact_info', bash_command='wget -O /shared-volume/ontario-school-data/' + public_school_contact_info_dllink.split("/")[-1] + ' ' + public_school_contact_info_dllink)
        download_private_school_contact_info = BashOperator(task_id='download_private_school_contact_info', bash_command='wget -O /shared-volume/ontario-school-data/' + private_school_contact_info_dlink.split("/")[-1] + ' ' + private_school_contact_info_dlink)
        download_academic_year = BashOperator(task_id='download_academic_year', bash_command='wget -O /shared-volume/ontario-school-data/'+ academic_year_dlink.split("/")[-1] + ' ' + academic_year_dlink)
        download_school_info_student_demographics = BashOperator(task_id='download_school_info_student_demographics', bash_command='wget -O /shared-volume/ontario-school-data/'+ school_info_student_demographics_dlink.split("/")[-1] + ' ' + school_info_student_demographics_dlink)
        
        # Upload files to HDFS
        upload_school_board_school_authority_contact = PythonOperator(task_id='upload_school_board_school_authority_contact', python_callable=upload_to_hdfs, op_kwargs={'fileName': school_board_school_authority_contact_dlink.split("/")[-1]}, dag=dag)
        upload_public_school_contact_info = PythonOperator(task_id='upload_public_school_contact_info', python_callable=upload_to_hdfs, op_kwargs={'fileName': public_school_contact_info_dllink.split("/")[-1]}, dag=dag)
        upload_private_school_contact_info = PythonOperator(task_id='upload_private_school_contact_info', python_callable=upload_to_hdfs, op_kwargs={'fileName': private_school_contact_info_dlink.split("/")[-1]}, dag=dag)
        upload_academic_year = PythonOperator(task_id='upload_academic_year_dlink', python_callable=upload_to_hdfs, op_kwargs={'fileName': academic_year_dlink.split("/")[-1]}, dag=dag)
        upload_school_info_student_demographics = PythonOperator(task_id='upload_school_info_student_demographics', python_callable=upload_to_hdfs, op_kwargs={'fileName': school_info_student_demographics_dlink.split("/")[-1]}, dag=dag)

        download_school_board_school_authority_contact >> upload_school_board_school_authority_contact
        download_public_school_contact_info >> upload_public_school_contact_info
        download_private_school_contact_info >> upload_private_school_contact_info
        download_academic_year >> upload_academic_year
        download_school_info_student_demographics >> upload_school_info_student_demographics
