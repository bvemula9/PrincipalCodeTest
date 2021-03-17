import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


client = boto3.client('glue', region_name='us-east-2')

source_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "path": "s3://csvconverterbv/test.csv"
    },
    format="csv",
    transformation_ctx="source_df"
    )

out_df = glueContext.write_dynamic_frame.from_options(
    frame=source_df,
    connection_type="s3",
    connection_options={
        "path": "s3://csvconverterbv/test.paraquet"
        },
    format="parquet",
    transformation_ctx="out_df"
    )
job.commit()
