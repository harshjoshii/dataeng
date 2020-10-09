from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType
from pyspark_lib import GenericSparkOperations, format_website_link, extract_street_number
from pyspark_lib import extract_street_name, format_postal_code, format_string_to_title_case

shared_volume_path = "/shared_volume/ontario_school_data/"
spark_master = "spark://spark-master:7077"
files = {"prsc": "private_schools_contact_information_september_2020_en.csv", \
        "prscs1": "private_schools_contact_information_september_2020_en_s1.csv"}

# Cleaning and Transformation steps for private_schools_contact_information_september_2020_en
def transform_private_schools_contact_information():

        app_name = "Private Schools Info Transformation"
        spark = GenericSparkOperations(spark_master, app_name)

        print("Reading file...")
        df = spark.read_file(shared_volume_path, files['prsc'])
        print("Reading complete")

        # 1. School website column renamed to Website and link should be starting with www.
        df_website_added = df.withColumn('Website', format_website_link(col('School Website')))
        df_school_website_removed = df_website_added.drop('School Website')

        # 2. Split street name and number from the street address column
        df_street_no_added = df_school_website_removed.withColumn('Street No', extract_street_number(col('Street Address')))
        df_street_name_added = df_street_no_added.withColumn('Street Name', extract_street_name(col('Street Address')))
        df_street_addr_removed = df_street_name_added.drop('Street Address')

        # 3. Change format for the Postal Code
        df_postal_code_formatted = df_street_addr_removed.withColumn('PostalCode', format_postal_code(col('Postal Code')))
        df_postal_code_removed = df_postal_code_formatted.drop('Postal Code')
        df_postal_code_renamed = df_postal_code_removed.withColumnRenamed('PostalCode', 'Postal Code')

        # 4. City column should be all in Title Case
        df_city_formatted = df_postal_code_renamed.withColumn('CityN', format_string_to_title_case(col('City')))
        df_city_removed = df_city_formatted.drop('City')
        df_city_renamed = df_city_removed.withColumnRenamed('CityN', 'City')

        # 5. Principal Name column should be all in Title Case
        df_principal_name_formatted = df_city_renamed.withColumn('PrincipalName', format_string_to_title_case(col('Principal Name')))
        df_principal_name_removed = df_principal_name_formatted.drop('Principal Name')
        df_principal_name_renamed = df_principal_name_removed.withColumnRenamed('PrincipalName', 'Principal Name')
        
        print("Writing file...")
        spark.create_file(shared_volume_path, files['prsc'].split(".")[0]+"_transformed", df_principal_name_renamed)
        print("Writing complete")

        spark.stop()

# Cleaning and Transformation steps for private_schools_contact_information_september_2020_en_s1
def transform_private_schools_contact_information_s1():
        app_name = "Private Schools Info S1 Transformation"
        spark = GenericSparkOperations(spark_master, app_name)

        print("Reading file...")
        df = spark.read_file(shared_volume_path, files['prscs1'])
        print("Reading complete")

        # 1. Website column should all be starting with www.
        df_website_added = df.withColumn('WebsiteN', format_website_link(col('Website')))
        df_school_website_removed = df_website_added.drop('Website')
        df_school_website_renamed = df_school_website_removed.withColumnRenamed('WebsiteN', 'Website')

        print("Writing file...")
        spark.create_file(shared_volume_path, files['prscs1'].split(".")[0]+"_transformed.csv", df_school_website_renamed)
        print("Writing complete")

        spark.stop()

transform_private_schools_contact_information()
transform_private_schools_contact_information_s1()