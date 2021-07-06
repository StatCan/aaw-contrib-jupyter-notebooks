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
###   daaas_storage.standard()      returns NULL
###   daaas_storage.premium()      returns NULL
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
###    daaas_storage.standard()
###    # daaas_storage.premium()
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
    library(RJSONIO)

    location = sprintf("/vault/secrets/minio-%s-tenant-1.json", storage_type)
    j <- fromJSON(location)
    url <-j[['MINIO_URL']]
    MINIO_URL <- j[['MINIO_URL']]
    MINIO_ACCESS_KEY <- j[['MINIO_ACCESS_KEY']]
    MINIO_SECRET_KEY <- j[['MINIO_SECRET_KEY']]

    ENDPOINT = gsub("https?://", "", MINIO_URL)

    Sys.setenv(
        "AWS_S3_ENDPOINT" =  ENDPOINT,
        "AWS_ACCESS_KEY_ID" = MINIO_ACCESS_KEY,
        "AWS_SECRET_ACCESS_KEY" = MINIO_SECRET_KEY,
        "AWS_DEFAULT_REGION" = "",
        "SECURE" = startsWith(j[['MINIO_URL']], "https")
    )
}


daaas_storage.standard <- function () {
    daaas_storage.__getClient__("standard")
}

daaas_storage.premium <- function () {
    daaas_storage.__getClient__("premium")
}
