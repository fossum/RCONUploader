FROM alpine

RUN apk update && \
    apk add python3 py3-pip git
RUN pip3 install --break-system-packages \
    git+https://github.com/fossum/rcon.git@feature/add-enforce-labels-flag \
    attrs \
    mysql-connector-python

# Dev needs
