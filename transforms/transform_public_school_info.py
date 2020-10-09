from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark_lib import GenericSparkOperations, format_website_link
from pyspark_lib import format_postal_code, format_string_to_title_case

shared_volume_path = "/shared_volume/ontario_school_data/"
spark_master = "spark://spark-master:7077"

files = {"pubsc": "publicly_funded_schools_xlsx_september_2020_en.csv"}

def transform_public_schools_contact_information():
        
        app_name = "Public Schools Info Transformation"
        spark = GenericSparkOperations(spark_master, app_name)

        print("Reading file...")
        df = spark.read_file(shared_volume_path, files['pubsc'])
        print("Reading complete")

        # 1. School website column should be starting with www.
        df_school_website_added = df.withColumn('Website', format_website_link(col('School Website')))
        df_school_website_removed = df_school_website_added.drop('School Website')
        df_school_website_renamed = df_school_website_removed.withColumnRenamed('Website', 'School Website')

        # 2. Board website column  should be starting with www.
        df_board_website_added = df_school_website_renamed.withColumn('Website', format_website_link(col('Board Website')))
        df_board_website_removed = df_board_website_added.drop('Board Website')
        df_board_website_renamed = df_board_website_removed.withColumnRenamed('Website', 'Board Website')

        # 3. Change format for the Postal Code
        df_postal_code_formatted = df_board_website_renamed.withColumn('PostalCode', format_postal_code(col('Postal Code')))
        df_postal_code_removed = df_postal_code_formatted.drop('Postal Code')
        df_postal_code_renamed = df_postal_code_removed.withColumnRenamed('PostalCode', 'Postal Code')

        # 4. City column should be all in Title Case
        df_city_formatted = df_postal_code_renamed.withColumn('CityN', format_string_to_title_case(col('City')))
        df_city_removed = df_city_formatted.drop('City')
        df_city_renamed = df_city_removed.withColumnRenamed('CityN', 'City')
        
        print("Writing file...")
        spark.create_file(shared_volume_path, files['pubsc'].split(".")[0]+"_transformed", df_city_renamed)
        print("Writing complete")

        spark.stop()

transform_public_schools_contact_information()