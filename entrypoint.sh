#!/bin/sh

# then run the CMD passed as command-line arguments
if [ "$#" -ne "0" ]; then
    exec "$@"
else
    exec "python3 ./main.py"
fi
