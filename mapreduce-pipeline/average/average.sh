#!/usr/bin/env bash

# Computes 4*average of one or more numbers provided as JSON input arguments
# 
# Intended use is for computing an estimate of pi by using in conjunction with 
# with sample.sh.

# Take an average to estimate pi.
#
# Input:
# (one of numbers and input_path must be specified)
#     --output   (optional) Output bucket/folder
#     --numbers  Sequence of JSON strings that each include the field "result"
#     --input_paths   Sequence of locations in minio to load results files from
#
# Output:
#     ./output/out.json
#         JSON of pi (4*average of inputs) and samples (n_inputs)


# Settings (probably don't need to change these)
HOST_ALIAS="ARIBTRARY-HOST-ALIAS-FOR-MINIO-MOUNT"
OUTPUT_LOCAL_DIR=./output
LOCAL_INPUT_STORAGE=./input.txt
MINIO_URL="http://$MINIO_URL"

# Remove input/output swap files, just in case (only really needed for local development)
rm -r $OUTPUT_LOCAL_DIR
rm $LOCAL_INPUT_STORAGE


# Helper function to connect to minio host (if not already connected)
connect_minio()
{
    if [ -z $MINIO_CONNECTED ]; then
      echo mc config host add $HOST_ALIAS \
            "$MINIO_URL" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"
        mc config host add $HOST_ALIAS \
            "$MINIO_URL" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"
        if [ $? -ne 0 ]
        then
            echo "Failed to push all files to minio.  Check above errors from minio"
            exit 1
        fi
        MINIO_CONNECTED=1

    fi
}


echo "Received command line args:"
echo $@
echo "---------------------------"


# Parse inputs

MINIO_PATHS=()

while test -n "$1"; do
    case "$1" in
        --output)
            shift
            OUTPUT="$1"
            ;;

        --json) 
            # store result from json in file
            shift
            printf '%d\n' $(jq -nr "$1 | .result") >> $LOCAL_INPUT_STORAGE

            ;;

        --minio_path) 
            # push minio url's to file for later use
            shift
            MINIO_PATHS+=($1)
            ;;

        *)
            echo "Invalid option $1; allowed: --params --options" >&2
            exit 1
            ;;
    esac
    shift
done


# For any input specified by minio, collect it and push it to the same 
# local input storage as for json
for mpath in ${MINIO_PATHS[@]}; 
do
    connect_minio

    # Not sure how to make the printf below show a failure code if mc fails, so test first then get
    mc ls "$HOST_ALIAS/$mpath"
    if [ $? -ne 0 ]
    then
        echo "Failed to push all files to minio.  Check above errors from minio"
        exit 1
    fi
    printf '%d\n' `mc cat "$HOST_ALIAS/$mpath" | jq .result` >> $LOCAL_INPUT_STORAGE

done


# Check that we have at least SOME data
if [ ! -s $LOCAL_INPUT_STORAGE ] 
then
    echo "Error: Found no inputs numbers for averaging"
    exit 1
fi


# Setup workspace
mkdir -p $OUTPUT_LOCAL_DIR


# Do the estimate of Pi, saved to out.json
awk '{sum+=$1} END {
    pi = 4*sum/NR;
    printf("{ \"pi\" : %.12f, \"samples\" : %d }\n", pi, NR);
}' $LOCAL_INPUT_STORAGE | jq '.' | tee $OUTPUT_LOCAL_DIR/out.json


# If required, push results to Minio
if [ -n "${OUTPUT}" ]
then
    # Ensure OUTPUT ends in a single /.  Minio doesn't like if there's multiple /'s
    # and we need at least one as this is a minio "directory"
    OUTPUT=`echo $OUTPUT | sed 's/\/*$/\//g'`

    echo "Push results to MINIO_URL: ${MINIO_URL}"
    connect_minio


    echo copying to minio storage with command:
    echo mc cp $OUTPUT_LOCAL_DIR/* "$HOST_ALIAS/$OUTPUT"
    mc cp $OUTPUT_LOCAL_DIR/* "$HOST_ALIAS/$OUTPUT"
    if [ $? -ne 0 ]
    then
        echo "Failed to push all files to minio.  Check above errors from minio"
        exit 1
    fi
fi


echo "Done."
