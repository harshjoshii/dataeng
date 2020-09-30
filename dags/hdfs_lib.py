import datetime as dt
from hdfs import InsecureClient

client_hdfs  = InsecureClient('http://namenode:9870')

def upload_to_hdfs(fileName):
    client_hdfs.upload("/dataeng/", "/shared-volume/ontario-school-data/"+fileName, chunk_size=65536, cleanup=True)
    


