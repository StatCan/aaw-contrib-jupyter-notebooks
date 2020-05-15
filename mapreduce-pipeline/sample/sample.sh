#!/usr/bin/env sh

# Randomly picks an (x,y) point inside a 2x2 square then returns 
# whether that point resides inside a unit circle (circle with r=1)
# centered in the square in an output file
#
# Doing this action repeatly and taking 4x(fraction_of_points_in_circle)
# gives an estimate of pi
#
# Random number generation here depends on a seed integer passed 
# as a parameter
#
# Input:
#     --params  Json string containing integer "seed"
#     --output  (optional) Output bucket/folder
#
# Output:
#     ./output/in.json
#         JSON of input parameters (received from --params)
#     ./output/out.json
#         JSON of (x, y) coordinates tested and "result" (0==outside, 
#         1==inside circle)
#     (note: local ./output location can be changed via OUTPUT_LOCAL_DIR)
#     If --output arg specified, output is also pushed to minio storage
#     at that location.  Minio credentials are defined via environment 
#     variables MINIO_URL, MINIO_ACCESS_KEY, and MINIO_SECRET_KEY


# Settings (probably don't need to change these)
HOST_ALIAS="ARIBTRARY-HOST-ALIAS-FOR-MINIO-MOUNT"
OUTPUT_LOCAL_DIR=./output


# Parse input arguments
while test -n "$1"; do
    case "$1" in
        --output)
            shift
            OUTPUT="$1"
            ;;

        --params)
            shift
            JSON="$1"
            ;;

        *)
            echo "Invalid option $1; allowed: --params --options" >&2
            exit 1
            ;;
    esac
    shift
done

# Check for required parameter params
if [ -z "$JSON" ] 
then
    echo "Missing required argument --params"
    exit 1
fi


# Log input and output
mkdir -p $OUTPUT_LOCAL_DIR
echo "Input: "
echo "$JSON" | jq '.' | tee $OUTPUT_LOCAL_DIR/in.json


# In the circle?
echo "Output: "
SEED=$(jq -rn "$JSON | .seed")
awk -v seed=$SEED 'BEGIN {
       srand(seed);
       x = rand() * 2 - 1;
       y = rand() * 2 - 1;
       result = (x*x + y*y <= 1);
       printf("{ \"x\" : %.3f, \"y\" : %.3f, \"result\" : %d }\n", x, y, result);
}' | tee $OUTPUT_LOCAL_DIR/out.json
echo "Result written to $OUTPUT_LOCAL_DIR/out.json"

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
