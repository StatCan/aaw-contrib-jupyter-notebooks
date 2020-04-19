#!/usr/bin/env python3


from kfp import dsl
from kubernetes import client as k8s_client
import os
import warnings; warnings.simplefilter('ignore')

minio_endpoint = os.environ.get('MINIO_URL', 'minio-service.kubeflow.svc.cluster.local:9000')
minio_key = os.environ.get('MINIO_KEY', 'minio')
minio_secret = os.environ.get('MINIO_SECRET', 'XXXXXX')

print(f'''
Minio parameters : URL {minio_endpoint}
key : {minio_key}
secret : {minio_secret}
''')

os.environ['AWS_ACCESS_KEY_ID'] = minio_key
os.environ['AWS_SECRET_ACCESS_KEY'] = minio_secret
os.environ['AWS_REGION'] = 'us-west-1'
os.environ['S3_REGION'] = 'us-west-1'
os.environ['S3_ENDPOINT'] = minio_endpoint
os.environ['S3_USE_HTTPS'] = '0'
os.environ['S3_VERIFY_SSL'] = '0'


def inject_env_var(var):
    dsl.get_pipeline_conf().add_op_transformer(
        lambda cop: cop.container.add_env_variable(
            k8s_client.V1EnvVar(
                name=var,
                value=os.environ[var]
            )
        )
    )

def inject_env_vars():
    dsl.get_pipeline_conf().set_image_pull_secrets([
        k8s_client.V1ObjectReference(
            name="k8scc01covidacr-registry-connection")])
    for var in (
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_REGION',
        'S3_REGION',
        'S3_ENDPOINT',
        'S3_USE_HTTPS',
        'S3_VERIFY_SSL'
    ):
        inject_env_var(var)


def make_bucket(bucket):
    from minio import Minio
    from minio.error import ResponseError

    s3Client = Minio(minio_endpoint,
                 access_key=minio_key,
                     secret_key=minio_secret,
                     secure=False)

    if not s3Client.bucket_exists(bucket):
        s3Client.make_bucket(bucket, location=os.environ['AWS_REGION'])


# Do I have to do this in the pipeline call?
# Or can I do it here?
#inject_env_vars()

