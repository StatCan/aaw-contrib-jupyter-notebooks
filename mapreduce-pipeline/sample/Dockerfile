FROM alpine

RUN apk add --no-cache wget jq bash
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x mc && \
    mv mc /usr/bin/

COPY sample.sh /sample.sh
ENTRYPOINT ["/sample.sh"]
