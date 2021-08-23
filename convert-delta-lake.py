"""

author@Kyle E.


This code takes a path from your Data Lake and converts it to 'delta' format which is a pre-requisite for this.

Feel free to edit the file formats. For this demo, we will use a standard csv file

"""

from delta import *
from pyspark.sql.session import SparkSession


spark = SparkSession \
    .builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()


# Read Source
inputDF = spark.read.format("csv").option("header", "true").load('s3://delta-lake-aws-glue-demo/raw/')

# Write data as a DELTA TABLE
inputDF.write.format("delta").mode("overwrite").save("s3a://delta-lake-aws-glue-demo/current/")

# Read Source
updatesDF = spark.read.format("csv").option("header", "true").load('s3://delta-lake-aws-glue-demo/updates/')

# Write data as a DELTA TABLE
updatesDF.write.format("delta").mode("overwrite").save("s3a://delta-lake-aws-glue-demo/updates_delta/")

# Generate MANIFEST file for Athena/Catalog
deltaTable = DeltaTable.forPath(spark, "s3a://delta-lake-aws-glue-demo/current/")
deltaTable.generate("symlink_format_manifest")

### OPTIONAL, UNCOMMENT IF YOU WANT TO VIEW ALSO THE DATA FOR UPDATES IN ATHENA
###
# Generate MANIFEST file for Updates
# updatesDeltaTable = DeltaTable.forPath(spark, "s3a://delta-lake-aws-glue-demo/updates_delta/")
# updatesDeltaTable.generate("symlink_format_manifest")
