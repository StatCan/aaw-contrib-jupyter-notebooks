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
###  minio_client =  get_minimal_client()      # return a Minio object 
###  minio_client =  get_pachyderm_client()    # return a Minio object  
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
###    minio_client = get_minimal_client():
###    # minio_client = get_pachyderm_client():    
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

def __get_minio_client__(tenant):
    """ Get the variables out of vault to create Minio Client. """

    d = {
        'MINIO_URL'        : None,
        'MINIO_ACCESS_KEY' : None,
        'MINIO_SECRET_KEY' : None
    }

    if tenant not in ("minimal", "premium", "pachyderm"):
        print("Not a valid resource! Options are")
        print("minimal, premium, pachyderm.")
        print("We will try anyway...")

    vault = f"/vault/secrets/minio-{tenant}-tenant1"

    for var in d: 
        CMD = f'echo $(source {vault}; echo ${var})'
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True,
                             executable='/bin/bash')
        d[var] = p.stdout.readlines()[0].strip().decode("utf-8")

    import re
    # Get rid of http:// in minio URL
    http = re.compile('^https?://')
        
    # Create the minio client.
    s3Client = Minio(
        http.sub("", d['MINIO_URL']),
        access_key=d['MINIO_ACCESS_KEY'],
        secret_key=d['MINIO_SECRET_KEY'],
        secure=False,
        region="us-west-1"
    )

    return s3Client



def get_minimal_client():
    """Get a connection to the minimal Minio tenant"""
    return __get_minio_client__("minimal")

def get_pachyderm_client():    
    """Get a connection to the pachyderm Minio tenant"""
    return __get_minio_client__("pachyderm")

def get_premium_client():
    """Get a connection to the premium Minio tenant"""
    return __get_minio_client__("premium")
