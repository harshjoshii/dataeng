from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark_lib import GenericSparkOperations, format_website_link, format_postal_code
from pyspark_lib import extract_street_name, extract_street_number

shared_volume_path = "/shared_volume/ontario_school_data/"
spark_master = "spark://spark-master:7077"

files = {"bsa": "boards_schoolauthorities_september_2020_en.csv"}

def transform_boards_information():
        
        app_name = "Boards Info Transformation"
        spark = GenericSparkOperations(spark_master, app_name)

        print("Reading file...")
        df = spark.read_file(shared_volume_path, files['bsa'])
        print("Reading complete")

        # 1. Website column should all be starting with www.
        df_website_added = df.withColumn('WebsiteN', format_website_link(col('Website')))
        df_website_removed = df_website_added.drop('Website')
        df_website_renamed = df_website_removed.withColumnRenamed('WebsiteN', 'Website')

        # 3. Change format for the Postal Code
        df_postal_code_formatted = df_website_renamed.withColumn('PostalCode', format_postal_code(col('Postal Code')))
        df_postal_code_removed = df_postal_code_formatted.drop('Postal Code')
        df_postal_code_renamed = df_postal_code_removed.withColumnRenamed('PostalCode', 'Postal Code')

        # 4. Remove the Suite column
        df_suite_removed = df_postal_code_renamed.drop('Suite')

        # 5. Split street name and number from the street address column
        df_street_no_added = df_suite_removed.withColumn('Street No', extract_street_number(col('Street')))
        df_street_name_added = df_street_no_added.withColumn('Street Name', extract_street_name(col('Street')))
        df_street_addr_removed = df_street_name_added.drop('Street')
        
        print("Writing file...")
        spark.create_file(shared_volume_path, files['bsa'].split(".")[0]+"_transformed", df_street_addr_removed)
        print("Writing complete")

        spark.stop()

transform_boards_information()