"""

author@Kyle E.


This code takes a Delta Lake table and does an INSERT operation using Spark SQL.


"""

from delta import *
from pyspark.sql.session import SparkSession


spark = SparkSession \
    .builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()


insertDF = spark.sql("""

INSERT INTO delta.`s3a://delta-lake-aws-glue-demo/current/`
SELECT *
FROM delta.`s3a://delta-lake-aws-glue-demo/updates_delta/`
WHERE CAST(row_id as integer) <= 20

""")

# Generate MANIFEST file for Athena/Catalog
deltaTable = DeltaTable.forPath(
    spark, "s3a://delta-lake-aws-glue-demo/current/")
deltaTable.generate("symlink_format_manifest")

### OPTIONAL
## SQL-BASED GENERATION OF SYMLINK MANIFEST

# spark.sql("""

# GENERATE symlink_format_manifest 
# FOR TABLE delta.`s3a://delta-lake-aws-glue-demo/current/`

# """)
