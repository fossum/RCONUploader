FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt update && \
    apt install openssh-client python3 python3-pip python3-venv libmariadb-dev -y
# RUN pip3 install --break-system-packages \
#     git+https://github.com/fossum/rcon.git@feature/add-enforce-labels-flag \
#     attrs \
#     mysql-connector-python

# Add Code
ADD ./entrypoint.sh /uploader/
ADD ./*.py /uploader/
ADD ./databases/*.py /uploader/databases/

# Run it
WORKDIR /uploader
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
