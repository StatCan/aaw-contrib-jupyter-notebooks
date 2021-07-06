#!/usr/bin/env python3

###################################
#
#  Download data into PowerBI through SQL
#  ======================================
#
#  BEFORE YOU RUN THIS:
#
#      1. Install boto3, pandas, and numpy.
#
#         - Open the windows command prompt (cmd)
#         - Run "conda activate azureml_py36_automl"
#         - Run "conda install pandas numpy boto3"
#
#      2. Set PowerBI's Python to azureml_py36_automl .
#
#         - Go to File -> Options and settings -> Options -> Python scripting
#         - Set a Python home directory to "C:\Miniconda\envs\azureml_py36_automl"
#
#
#      2.5. (Optional) Test your script in Python
#
#           - Copy this file to your Desktop and adjust it
#             to use your ACCESS_KEY and SECRET_KEY, and to
#             access your data/make your queries. Make sure
#             that your queries are returning what you want.
#
#      3. Run this script inside PowerBI
#
#         - Click "Get Data" and select "Python script"
#         - Copy paste your version of this script into the text box.
#         - Edit your script to at least include your ACCESS_KEY and SECRET_KEY.
#
#
#
#      NOTE: To get your ACCESS_KEY and SECRET_KEY, go here for instructions.
#
#            https://statcan.github.io/daaas/en/Storage/#programmatic-access
#
#            Then `source /vault/secrets/minio-standard-tenant-1` and run
#
#                  $ echo $MINIO_ACCESS_KEY
#                  $ echo $MINIO_SECRET_KEY
#
#
#  edited: May 19, 2020
#
###################################

import boto3
from os import remove
import tempfile
import pandas as pd
import sys

#########################
#        CONFIG         #
#########################

TENANT = 'minimal' # options: standard, premium

# mandatory. Must get your credentials from Jupyter.
ACCESS_KEY = 'XXXXXXXX'
SECRET_KEY = 'YYYYYYYY'

#########################
#   Ignore this stuff   #
#  Skip to "your file"  #
#########################

def get_minio_client():
    """ create Minio Client. """
    # TODO: Accessing this from within the datacenter would be better.
    URL = f'https://standard-{TENANT}-tenant-1.covid.cloud.statcan.ca'
    SECURE = URL.startswith('https')
    return boto3.client('s3',
                  endpoint_url=URL,
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY,
                  use_ssl=SECURE,
                  region_name="us-west-1")

def __from_s3__(table_type):
    def get_from_json(r):
        """
        Read the response block by block as JSON,
        write to disk to keep memory from exploding.
        """
        temp = tempfile.NamedTemporaryFile(delete=False)
        for event in r['Payload']:
            if 'Records' in event:
                temp.write(event['Records']['Payload'])
        temp.close()
        resp = table_type(temp.name)
        try:
            remove(temp.name)
        except:
            print(f"""There was an error removing the file:\n{temp.name}\n... Proceeding anyway.""", file=sys.stderr)

        return resp
    return get_from_json

@__from_s3__
def pandas_from_json(r):
    """ Read the stream from s3 and turn JSON into a pandas Dataframe. """
    df = pd.read_json(r, lines=True)
    print("Created Dataframe with dimensions: (nrow, ncol) = %s" % str(df.shape), file=sys.stderr)
    return df

s3 = get_minio_client()

############################################################
############################################################
#                                           ~ edit below ~ #
#       YOUR FILE: Tweak the path,                         #
#                        the extension,                    #
#                        the query,                        #
#                    and the compression                   #
#                                                          #
############################################################
############################################################

BUCKET = 'shared'
r = s3.select_object_content(
    Bucket=BUCKET,
    Key='/blair-drummond/sql-example/TotalPopulation.csv.gz',
    ExpressionType='SQL',
    # Note, there's no ';' at the end.
    Expression="""
    SELECT PopTotal,PopDensity FROM s3object s
    WHERE s.Location like '%Canada%'
    """,
    InputSerialization={
        'CSV': {
            # Use this if your CSV file has a header. Else set to "NONE".
            "FileHeaderInfo": "USE",
            'RecordDelimiter': '\n',
            'FieldDelimiter': ',',
            ## There are more formatting options available, if they're needed.
        },
        # Remove this if the file isn't compressed.
        'CompressionType': 'GZIP',
    },
    # JSON is easier to work with than csv, unless you
    # have a massive amount of data.
    OutputSerialization={'JSON': {}},
    # OutputSerialization={'CSV': {'RecordDelimiter': '\n', 'FieldDelimiter': ','}},

)

# Using the CSV format is WAY faster, but you lose the column names!
# You can edit this.

df = pandas_from_json(r)
# df = pandas_from_csv(r)

print(df.head())

