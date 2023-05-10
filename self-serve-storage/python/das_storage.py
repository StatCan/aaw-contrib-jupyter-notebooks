#!/usr/bin/env python3

#########################################
###                                   ###
###          DAS_storage.py         ###
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
###  list =  get_instances()      # return all available MinIO instances
###  instances =  Instances()      # return an object which has all the MinIO Clients as attributes
###
###  See: https://github.com/minio/minio-py

###########################
###    Usage Example    ###
###########################
###
###    import DAS_storage.py
###
###    print(get_instances())   # to see what instances are available
###    instances = DAS_storage.Instances() 
###    storage = instances.minio_standard    # choose one of the instances that was printed
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

def get_client(instance):
    """ Get the variables out of vault to create Minio Client. """

    with open(f'/vault/secrets/{instance}.json') as f:
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

class Instances:
    clients = []

    def __init__(self):
        instance_list = get_instances()
        for i in instance_list:
            self.add_instance(i)      

    def add_instance(self, instance):
        self.clients.append(instance)
        # changes '-' to '_' in attribute name to create valid name
        setattr(self, instance.replace("-", "_"), get_client(instance))  
            
def get_instances():
    instances = [file for file in os.listdir('/vault/secrets') if not file.endswith('.json')]
    return instances
