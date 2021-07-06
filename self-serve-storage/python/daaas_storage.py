#!/usr/bin/env python3

#########################################
###                                   ###
###          daaas_storage.py         ###
###          ~~~~~~~~~~~~~~~~         ###
###                                   ###
###   Import this from your notebook  ###
###   to easily access your storage   ###
###                                   ###
#########################################

####################
###      API     ###
####################
###
###  minio_client =  get_standard_client()      # return a Minio object
###  minio_client =  get_premium_client()      # return a Minio object
###
###  See: https://github.com/minio/minio-py

###########################
###    Usage Example    ###
###########################
###
###    import daaas_storage.py
###
###    # Choose from
###    minio_client = get_standard_client():
###    # minio_client = get_premium_client():
###
###
###    # This minio client is from minio-py, and you can use it
###    # for and s3 purpose
###    # See https://github.com/minio/minio-py
###
###
###    # Example:
###    objects = minio_client.list_objects(
###        "shared",
###        prefix='blair-drummond/',
###        recursive=True
###          )
###
###    for obj in objects:
###        print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
###              obj.etag, obj.size, obj.content_type)
###
###

import subprocess
from minio import Minio
import os
import json

def __get_minio_client__(tenant):
    """ Get the variables out of vault to create Minio Client. """

    if tenant not in ("standard", "premium"):
        print("Not a valid resource! Options are")
        print("standard, premium")
        print("We will try anyway...")

    #vault = f"/vault/secrets/minio-{tenant}-tenant-1"

    with open(f'/vault/secrets/minio-{tenant}-tenant-1.json') as f:
        creds = json.load(f)
        minio_url = creds['MINIO_URL']

    import re
    # Get rid of http:// in minio URL
    http = re.compile('^https?://')

    # Create the minio client.
    s3Client = Minio(
        http.sub("", creds['MINIO_URL']),
        access_key=creds['MINIO_ACCESS_KEY'],
        secret_key=creds['MINIO_SECRET_KEY'],
        secure=minio_url.startswith('https'),
        region="us-west-1"
    )

    return s3Client


def get_standard_client():
    """Get a connection to the minimal Minio tenant"""
    return __get_minio_client__("standard")

def get_premium_client():
    """Get a connection to the premium Minio tenant"""
    return __get_minio_client__("premium")
