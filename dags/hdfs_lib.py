import datetime as dt
from hdfs import InsecureClient

client_hdfs  = InsecureClient('http://namenode:9870')

def upload_to_hdfs(file_name, file_path, hdfs_path):
    client_hdfs.upload(hdfs_path, file_path+file_name, chunk_size=65536, cleanup=True)
    


