import re

EXPERIMENT_NAME_RE = re.compile('^[0-9a-zA-Z_-]+$')
BUCKET_NAME_RE = re.compile('^[\/0-9a-z_-]+(?<!\/)$')
MINIO_PATH_RE = re.compile('^[0-9a-z_-]*[\/0-9a-z_-]+(?<!\/)$')

# Bucketname has letters, numbers, underscores, hyphens only
# Must not end in a slash (that will be added when needed)
bucketname = re.compile('^[\/0-9a-z_-]+(?<!\/)$')

def validate_kfp_name(s):
    """
    Return whether this is a valid kubeflow pipeline experiment/pipeline step name
    
    These names can contain alphanumeric characters, hyphens,
    or underscores
    """
    return EXPERIMENT_NAME_RE.match(s)

def validate_bucket_name(s):
    """
    Return whether this is a valid minio bucket name
    
    Bucketname has letters, numbers, underscores, hyphens only
    Must not end in a slash (that will be added when needed)
    """
    return BUCKET_NAME_RE.match(s)

def validate_minio_path(s):
    """
    Return whether this is a valid minio path
    
    same restrictions as bucketname except it can contain "/"
    but not start or end with a forward slash "/"
    """
    return MINIO_PATH_RE.match(s)