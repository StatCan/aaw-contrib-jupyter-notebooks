FROM alpine

RUN apk add --no-cache wget jq bash

COPY average.sh /average.sh
ENTRYPOINT ["/average.sh"]
