# aws-glue-delta-lake
This repository is for demonstrating the capability to do SQL-based UPDATES, DELETES, and INSERTS directly in the Data Lake using Amazon S3, AWS Glue and Delta Lake.

---


# Architecture Diagram

![Kyle-Escosia-AWS-Glue-Delta-Lake-Diagram](https://i.imgur.com/pZ4C9eh.png)


### athena-query.sql

Generates the schema for the Delta Table

### UPSERTS.py

This code takes a Delta Lake table and does an UPSERT operation using Spark SQL.

### DELETES.py

This code takes a Delta Lake table and does a DELETE operation using Spark SQL.

### INSERTS.py

This code takes a Delta Lake table and does an INSERT operation using Spark SQL.


