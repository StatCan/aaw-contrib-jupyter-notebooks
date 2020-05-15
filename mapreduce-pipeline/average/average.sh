#!/usr/bin/env sh

# Computes 4*average of one or more numbers provided as JSON input arguments
# 
# Intended use is for computing an estimate of pi by using in conjunction with 
# with sample.sh.

# Take an average to estimate pi.
#
# Input:
#     --numbers  Sequence of JSON strings that each include the field "result"
#     --output   (optional) Output bucket/folder
#
# Output:
#     ./output/out.json
#         JSON of pi (4*average of inputs) and samples (n_inputs)


# Settings (probably don't need to change these)
HOST_ALIAS="ARIBTRARY-HOST-ALIAS-FOR-MINIO-MOUNT"
OUTPUT_LOCAL_DIR=./output
LOCAL_INPUT_STORAGE=./input.txt

# Remove input/output swap files, just in case (only really needed for local development)
rm $LOCAL_INPUT_STORAGE
rm -rf $OUTPUT_LOCAL_DIR


# Parse inputs
while test -n "$1"; do
    case "$1" in
        --output)
            shift
            OUTPUT="$1"
            ;;

        --numbers) ;;
        # push .result from JSON numbers to a file for later use
            
        *)
            printf '%d\n' $(jq -nr "$1 | .result") >> $LOCAL_INPUT_STORAGE
            ;;
    esac
    shift
done


# Check for required data
if [ ! -s $LOCAL_INPUT_STORAGE ] 
then
    echo "Error: Found no inputs numbers for averaging"
    exit 1
fi


# Setup workspace
mkdir -p $OUTPUT_LOCAL_DIR


# Do the estimate of Pi
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
    echo mc config host add $HOST_ALIAS \
        "$MINIO_URL" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

    mc config host add $HOST_ALIAS \
        "$MINIO_URL" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

    echo copying to minio storage with command:
    echo mc cp $OUTPUT_LOCAL_DIR/* "$HOST_ALIAS/$OUTPUT"
    mc cp $OUTPUT_LOCAL_DIR/* "$HOST_ALIAS/$OUTPUT"
    # Test for success
    if [ $? -ne 0 ]
    then
        echo "Failed to push all files to minio.  Check above errors from minio"
        exit 1
    fi
fi


echo "Done."
