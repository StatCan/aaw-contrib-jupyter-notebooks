#!/usr/bin/env sh

# Take an average to estimate pi.
#
# Input:
#     --output   Output bucket/folder
#     --numbers  Sequence of JSON with field "result"
#
# Output:
#     pi.json
#
#     pi.json has as "pi" field and a "samples" field.
#
# Blair Drummond

mkdir -p /output

while test -n "$1"; do
    case "$1" in
        --output)
            shift
            OUTPUT="$1"
            ;;

        --numbers) ;;

        *)
            printf '%d\n' $(jq -nr "$1 | .result") >> /results.txt
            ;;
    esac
    shift
done

awk '{sum+=$1} END {
    pi = sum/NR;
    printf("{ \"pi\" : %.12f, \"samples\" : %d }\n", pi, NR);
}' /results.txt | jq '.' | tee /output/pi.json

echo "MINIO: -> _${S3_ENDPOINT}_"
mc config host add daaas \
    "http://$S3_ENDPOINT" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY"

echo mc cp -r /output "daaas/$OUTPUT"
mc cp -r /output "daaas/$OUTPUT"

echo "Done."
