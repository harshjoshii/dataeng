import os
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark_lib import GenericOperations

shared_volume_path = "/shared_volume/ontario_school_data/"
spark_master = "spark://spark-master:7077"
app_name = "DataTransformation"
files = {"bsa": "boards_schoolauthorities_september_2020_en.csv", \
        "pubsc": "publicly_funded_schools_xlsx_september_2020_en.csv", \
        "prsc": "private_schools_contact_information_september_2020_en.csv", \
        "prscs1": "private_schools_contact_information_september_2020_en_s1.csv"}

spark = GenericOperations(spark_master, app_name)

def transform_private_schools_contact_information():
    
# Cleaning and Transformation steps for private_schools_contact_information_september_2020_en
# 1. School website column should all be starting with www.
# 2. Split street name and number from the street address column
# 3. Change format for the Postal Code
# 4. Website column should all be starting with www.
# 5. City & Principal Name column should be all in Camel Case


# Cleaning and Transformation steps for boards_schoolauthorities_september_2020_en.csv
# 1. Split street name and number from the street address column
# 2. Remove the Suite column
# 3. Change format for the Postal Code
# 4. Website column should all be starting with www.

# Cleaning and Transformation steps for private_schools_contact_information_september_2020_en_s1
# 1. Website column should all be starting with www.

# Cleaning and Transformation steps for publicly_funded_schools_xlsx_september_2020_en
# 1. City column should be all in Camel Case
# 2. Change format for the Postal Code
# 3. School website and Board website column should all be starting with www.