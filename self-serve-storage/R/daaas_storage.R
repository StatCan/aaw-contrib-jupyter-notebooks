#########################################
###                                   ###
###          daaas_storage.R          ###
###          ~~~~~~~~~~~~~~~          ###
###                                   ###
###   Source this from your notebook  ###
###   to easily access your storage   ###
###                                   ###
#########################################

###########################
###         API         ###
###########################
###
###   daaas_storage.minimal()      returns NULL
###   daaas_storage.premium()      returns NULL
###   daaas_storage.pachyderm()    returns NULL
###
###

###########################
###    Usage Example    ###
###########################
###
###    source("daaas_storage.R")
###
###    # Choose from
###
###    daaas_storage.minimal()
###    # daaas_storage.premium()
###    # daaas_storage.pachyderm()
###
###    ### Note, unlike the python version, these functions 
###    ### modify the global option, instead of returning a
###    ### connection.
###
###    # Example:
###    get_bucket(bucket = "shared", use_https=FALSE, region="")
###

# Source the s3 storage secrets and urls.
get_bash_variable <- function (location, var) {
    system(
        sprintf(
            "bash -c 'source %s; echo $%s'",
            location,
            var
        ), 
        intern = TRUE
    )
}

### Just sets the environment variables.
daaas_storage.__getClient__ <- function (storage_type) {

    location = sprintf("/vault/secrets/minio-%s-tenant1", storage_type)

    MINIO_URL        = get_bash_variable(location, "MINIO_URL")
    MINIO_ACCESS_KEY = get_bash_variable(location, "MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = get_bash_variable(location, "MINIO_SECRET_KEY")
    
    ENDPOINT = gsub("https?://", "", MINIO_URL)

    Sys.setenv(
        "AWS_S3_ENDPOINT" =  ENDPOINT,
        "AWS_ACCESS_KEY_ID" = MINIO_ACCESS_KEY,
        "AWS_SECRET_ACCESS_KEY" = MINIO_SECRET_KEY,
        "AWS_DEFAULT_REGION" = ""
    )
}

    
daaas_storage.minimal <- function () {
    daaas_storage.__getClient__("minimal")
}
    
daaas_storage.premium <- function () {
    daaas_storage.__getClient__("premium")
}
    
daaas_storage.pachyderm <- function () {
    daaas_storage.__getClient__("pachyderm")
}
    
