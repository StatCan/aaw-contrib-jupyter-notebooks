#!/usr/bin/env bash

# Randomly picks an (x,y) point inside a 2x2 square returns 
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
# 
# Output:
#     ./output/in.json
#         JSON of input parameters (received from --params)
#     ./output/out.json
#         JSON of (x, y) coordinates tested and "result" (0==outside, 
#         1==inside circle)
#     (note: local ./output location can be changed by editing
#     OUTPUT_LOCAL_DIR)

echo "Received command line args:"
echo $@
echo "---------------------------"

# Settings (probably don't need to change these)
OUTPUT_LOCAL_DIR=./output

# Remove previous output, just in case (only really needed for local development)
rm -r $OUTPUT_LOCAL_DIR

# Parse input arguments
while test -n "$1"; do
    case "$1" in
        --params)
            shift
            JSON="$1"
            ;;

        *)
            echo "Invalid option $1; allowed: --params" >&2
            exit 1
            ;;
    esac
    shift
done

# Log input and create output location
mkdir -p $OUTPUT_LOCAL_DIR
echo "Input: "
echo "$JSON" | jq '.' | tee $OUTPUT_LOCAL_DIR/in.json

# In the circle?
echo "Output: "
SEED=$(jq -rn "$JSON | .seed")
if [ $? -ne 0 ]
then
    echo "Invalid input to --params.  Must be a json string with key of seed"
    exit 1
fi

# Put a point in a circle!
awk -v seed=$SEED 'BEGIN {
       srand(seed);
       x = rand() * 2 - 1;
       y = rand() * 2 - 1;
       result = (x*x + y*y <= 1);
       printf("{ \"x\" : %.3f, \"y\" : %.3f, \"result\" : %d }\n", x, y, result);
}' | tee $OUTPUT_LOCAL_DIR/out.json
echo "Result written to $OUTPUT_LOCAL_DIR/out.json"

echo "Done."
