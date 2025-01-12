FROM ubuntu:noble

RUN CODENAME=noble && \
    echo "deb http://truenas.thefoss.org:9142/ubuntu/ $CODENAME main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb http://truenas.thefoss.org:9142/ubuntu/ $CODENAME-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://truenas.thefoss.org:9142/ubuntu/ $CODENAME-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://truenas.thefoss.org:9142/ubuntu/ $CODENAME-backports main restricted universe multiverse" >> /etc/apt/sources.list

# Always use local if available (even if it's outdated).
RUN { \
    echo 'Package: *'; \
    echo 'Pin: origin "truenas.thefoss.org:9142"'; \
    echo 'Pin-Priority: 1001'; \
} >> /etc/apt/preferences.d/truenas-preferences

COPY requirements.txt /uploader/

RUN apt-get update && \
    apt-get install --no-install-recommends \
    git openssh-client python3 python3-pip \
    python3-venv libmariadb-dev \
    build-essential python-dev-is-python3 \
    -y

# Add Code
COPY ./entrypoint.sh /uploader/
COPY ./*.py /uploader/
COPY ./databases /uploader/databases
COPY ./games /uploader/games

# Set the working directory.
WORKDIR /uploader

# Create the Python virtual environment.
RUN mkdir -p .venv \
    && python3 -m venv .venv \
    && . .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install --no-cache-dir --requirement /uploader/requirements.txt

# Run it
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
