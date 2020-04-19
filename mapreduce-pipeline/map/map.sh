#!/usr/bin/env sh

# Compute pi.
#
# Input:
#     --output  Output bucket/folder
#     --params  Json containing integer "seed"
#
# Output:
#     in.json and out.json
#
#     out.json has as "result" field, which is 0 or 1, depending
#     on whether the random point is inside or outside the circle.
#
# Blair Drummond
#

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


# Log input and output
mkdir -p /output
echo "Input: "
echo "$JSON" | jq '.' | tee /output/in.json


# In the circle?
echo "Output: "
SEED=$(jq -rn "$JSON | .seed")
awk -v seed=$SEED 'BEGIN {
       srand(seed);
       x = rand() * 2 - 1;
       y = rand() * 2 - 1;
       result = 4 * (x*x + y*y <= 1);
       printf("{ \"x\" : %.3f, \"y\" : %.3f, \"result\" : %d }\n", x, y, result);
}' | tee /output/out.json


echo "MINIO: -> _${S3_ENDPOINT}_"
mc config host add daaas \
    "http://$S3_ENDPOINT" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY"

echo mc cp -r /output "daaas/$OUTPUT"
mc cp -r /output "daaas/$OUTPUT"

echo "Done."
