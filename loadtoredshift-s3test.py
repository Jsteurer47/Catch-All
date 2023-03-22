import psycopg2
import config
import boto3
import pypyodbc
import csv

Local_File = '\\page\data\Shipping\Groups\ShipExec\Distribution Procedure\Analyst\Jordan\FreightClaims\claims.txt'
Bucket_Filename = 'claims.txt'
bucket_name = 'colonydev'
folder_name = 'Operations'
key = folder_name + '/' + Bucket_Filename
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.upload_file(Local_File, key)
print ("Uploaded S3 successfully")
#Upload to redshift from S3
def redshift():
    conn = psycopg2.connect(dbname='edw', host='redshift.sccompanies.com', port='5439', user='cbedw', password=config.password)
    cur = conn.cursor()
    ##Begin your transaction
    cur.execute("begin;")
    cur.execute(""" TRUNCATE tempwork.FreightClaims;
    Copy tempwork.FreightClaims (
claimid,
vendorname,
pronumber,
housebillnumber,
ponum,companyid,
invoicenumber,
invoicedate,
carrierid,
carriername,
carrieraddress,
carriercitystatezip,
status,
reason,
amount,
IncidentNumber,
CarrierclaimNum,
comments,
keywordbucket,
formentrybucket,
paid,claimdate,
type,
attachments

)
from 's3://colonydev/Operations/claims.txt'
credentials 'aws_access_key_id={};aws_secret_access_key={}'   
delimiter ',' region 'us-east-1' ACCEPTINVCHARS REMOVEQUOTES TRIMBLANKS TRUNCATECOLUMNS COMPUPDATE ON dateformat 'auto' timeformat 'auto'"""\
    .format(config.aws_access_key_id, config.aws_secret_access_key))
    ##Commit your transaction
    cur.execute("commit;")
    print("Copy to Redshift executed fine!")
redshift()