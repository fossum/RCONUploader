FROM alpine

RUN apk update && \
    apk add python3 py3-pip

# Dev needs
RUN apk add git
