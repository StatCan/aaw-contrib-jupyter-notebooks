#!/usr/bin/env bash

# Computes 4*average of one or more numbers provided as JSON strings
# 
# Intended use is for computing an estimate of pi by using in conjunction with 
# with sample.sh.
# 
# Take an average to estimate pi.
#
# Input:
#     --numbers  Sequence of JSON strings that each include the field "result"
#
# Output:
#     ./output/out.json
#         JSON of pi (4*average of inputs) and samples (n_inputs)

echo "Received command line args:"
echo $@
echo "---------------------------"

# Settings (probably don't need to change these)
OUTPUT_LOCAL_DIR=./output
LOCAL_INPUT_STORAGE=./input.txt

# Remove input/output swap files, just in case (only really needed for local development)
rm -r $OUTPUT_LOCAL_DIR
rm $LOCAL_INPUT_STORAGE

# Parse inputs
while test -n "$1"; do
    case "$1" in
        --json) 
            # store result from json in file
            shift
            printf '%d\n' $(jq -nr "$1 | .result") >> $LOCAL_INPUT_STORAGE
            ;;

        *)
            echo "Invalid option $1; allowed: --json" >&2
            exit 1
            ;;
    esac
    shift
done


# Validate input
if [ ! -s $LOCAL_INPUT_STORAGE ] 
then
    echo "Error: Found no inputs numbers for averaging"
    exit 1
fi

# Setup workspace
mkdir -p $OUTPUT_LOCAL_DIR

# Estimate pi and save to out.json
awk '{sum+=$1} END {
    pi = 4*sum/NR;
    printf("{ \"pi\" : %.12f, \"samples\" : %d }\n", pi, NR);
}' $LOCAL_INPUT_STORAGE | jq '.' | tee $OUTPUT_LOCAL_DIR/out.json

echo "Done."
