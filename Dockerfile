FROM ubuntu

ADD requirements.txt /uploader/

RUN apt update && \
    apt install git openssh-client python3 python3-pip python3-venv libmariadb-dev -y
RUN pip3 install --break-system-packages \
    git+https://github.com/fossum/rcon.git@feature/add-enforce-labels-flag
RUN pip3 install --no-cache-dir --break-system-packages \
    --requirement /uploader/requirements.txt

# Add Code
ADD ./entrypoint.sh /uploader/
ADD ./*.py /uploader/
ADD ./databases /uploader/databases
ADD ./games /uploader/games

# Run it
WORKDIR /uploader
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
