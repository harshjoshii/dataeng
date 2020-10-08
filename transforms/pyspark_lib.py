import os
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

class GenericSparkOperations:
    def __init__(self, master, app_name):
        self.spark = SparkSession.builder \
                        .master(master) \
                        .appName(app_name) \
                        .getOrCreate()
    
    def read_file(self, file_path, file_name):
        if(os.path.exists(file_path)):
            file_path = os.path.join(file_path, file_name)
            df = self.spark.read.option("header", "true") \
                    .option("inferSchema", "true") \
                    .csv(file_path)
            return df
        else:
            raise FileNotFoundError("File path doesn't exist")
    
    def create_file(self, file_path, file_name, df):
        try:
            file_path = os.path.join(file_path, file_name)
            df.repartition(1).write.csv(file_path, header=True)
        except:
            print("There is some problem writing the file")
        else:
            print("File created successfully")

    def stop(self):
        self.spark.stop()

@udf(returnType=StringType())
def format_website_link(link):
    link = str(link)
    if not re.search("^www.", link) and link != "None":
            if re.search("^http://", link):
                    sp = re.split("^http://", link)
                    if not re.search("^www.", sp[1]):
                            return "www." + sp[1]
                    else:
                            return sp[1]
            else:
                    return "www." + link
    return link

@udf(returnType=StringType())
def extract_street_number(addr):
    try:
        addr = str(addr)
        if addr != "":
            if addr.split(" ")[0] != "":
                strno = addr.split(" ")[0]
                int(strno)
                return strno.strip()
            else:
                return "-"
        else:
            return "-"
    except:
        return "-"

@udf(returnType=StringType())
def extract_street_name(addr):
    try:
        addr = str(addr)
        if addr != "":
            if addr.split(" ")[0] != "":
                strno = addr.split(" ")[0]
                int(strno)
                return " ".join(addr.split(" ")[1:])
            else:
                return "-"
        else:
            return "-"
    except:
        return addr

@udf(returnType=StringType())
def format_postal_code(code):
    try:
        code = str(code)
        return code[0:3] + "-" + code[3:]
    except:
        return code

@udf(returnType=StringType())
def format_string_to_title_case(astr):
    try:
        astr = str(astr)
        return astr.title()
    except:
        return astr 


        