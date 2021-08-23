"""

author@Kyle E.


This code takes a Delta Lake table and does an UPSERT operation using Spark SQL.


"""

from delta import *
from pyspark.sql.session import SparkSession


spark = SparkSession \
    .builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()


updateDF = spark.sql("""

MERGE INTO delta.`s3a://delta-lake-aws-glue-demo/current/` as superstore
USING delta.`s3a://delta-lake-aws-glue-demo/updates_delta/` as updates
ON superstore.row_id = updates.row_id
WHEN MATCHED THEN
  UPDATE SET *
WHEN NOT MATCHED
  THEN INSERT *

""")

# Generate MANIFEST file for Athena/Catalog
deltaTable = DeltaTable.forPath(spark, "s3a://delta-lake-aws-glue-demo/current/")
deltaTable.generate("symlink_format_manifest")

### OPTIONAL
## SQL-BASED GENERATION OF SYMLINK

spark.sql("""

GENERATE symlink_format_manifest 
FOR TABLE delta.`s3a://delta-lake-aws-glue-demo/current/`

""")
