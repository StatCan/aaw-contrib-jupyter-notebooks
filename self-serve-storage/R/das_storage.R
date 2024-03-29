#########################################
###                                   ###
###          das_storage.R          ###
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
###   das_storage.get_client()      returns NULL
###   das_storage.get_instances()      returns NULL
###
###

###########################
###    Usage Example    ###
###########################
###
###    source("das_storage.R")
###
###    # Choose from
###
###    das_storage.get_client(instance) 
###    das_storage.get_instances()
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
        paste("bash -c 'source ", location, "; echo ", var, "'", sep = ""),
        intern = TRUE
    )
}
# Just sets the environment variables.
das_storage.get_client<- function(instance) {
    env_vars <- c("MINIO_URL", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY")
    location <- paste("/vault/secrets/", instance, sep = "")
    minio <- if (requireNamespace("jsonlite", quietly = TRUE)) {
        # jsonlite is installed on the AAW's R image
        # works just as well with RJSONIO::fromJSON or rjson::fromJSON
        jsonlite::fromJSON(paste0(location, ".json"))
    } else {
        lapply(setNames(nm = env_vars), function(x) {
            system(paste("bash -c 'source ", location, "; echo ", var, "'", sep = ""), intern = TRUE)
        })
    }
    Sys.setenv(
        "AWS_S3_ENDPOINT" = gsub("https?://", "", minio$MINIO_URL),
        "AWS_ACCESS_KEY_ID" = minio$MINIO_ACCESS_KEY,
        "AWS_SECRET_ACCESS_KEY" = minio$MINIO_SECRET_KEY,
        "AWS_DEFAULT_REGION" = "",
        "SECURE" = startsWith(minio$MINIO_URL, "https")
    )
}

# List MinIO instances
das_storage.get_instances <- function () {
    list <- grep(".*(?<!\\.json)$", list.files("/vault/secrets/"), perl=TRUE, value=TRUE)
    for (i in list) {
        print(i)
    }
}

