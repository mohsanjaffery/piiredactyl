import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


## get redaction field key from ssm
ssm = boto3.client('ssm', region_name='eu-west-1')
param = ssm.get_parameter(Name='redact_key')
params_csv = param['Parameter']['Value']


## get redaction regex from ssm
param = ssm.get_parameter(Name='redact_value')
redact_value = param['Parameter']['Value']


## @type: DataSource
## @args: [database = "cloudtrail_log_catalogue", table_name = "glue101raw", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "log_catalogue", table_name = "glue101raw", transformation_ctx = "datasource0")


## @type: ApplyMapping
## @args: [mapping = [("eventversion", "string", "eventversion", "string"), ("useridentity", "struct", "useridentity", "struct"), ("eventtime", "string", "eventtime", "string"), ("eventsource", "string", "eventsource", "string"), ("eventname", "string", "eventname", "string"), ("awsregion", "string", "awsregion", "string"), ("sourceipaddress", "string", "sourceipaddress", "string"), ("useragent", "string", "useragent", "string"), ("requestparameters", "struct", "requestparameters", "struct"), ("responseelements", "struct", "responseelements", "struct"), ("requestid", "string", "requestid", "string"), ("eventid", "string", "eventid", "string"), ("eventtype", "string", "eventtype", "string"), ("recipientaccountid", "string", "recipientaccountid", "string"), ("resources", "array", "resources", "array"), ("sharedeventid", "string", "sharedeventid", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
def mask_data(rec):
    keys = params_csv.split(',')
    kv = rec
    while len(keys) > 1:
        kv = kv.get(keys.pop(0))
    kv[keys.pop()] = redact_value
    return rec

applymapping1 =  Map.apply(frame = datasource0, f = mask_data)
print("==================================== BEGIN ======================================")
applymapping1.show(10)
print("==================================== END ======================================")


## @args: [connection_type = "s3", connection_options = {"path": "s3://glue.plentitu.de/transformed/cloudtrail"}, format = "json", transformation_ctx = "datasink2"]
## @return: datasink2
## @inputs: [frame = applymapping1]
datasink2 = glueContext.write_dynamic_frame.from_options(frame = applymapping1, connection_type = "s3", connection_options = {"path": "s3://piiredactyl-dev-data-transform/cloudtrail"}, format = "json", transformation_ctx = "datasink2")
job.commit()
