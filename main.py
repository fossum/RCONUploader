
from os import getenv
from rcon.source import Client

host = getenv('HOST', 'localhost')
port = int(getenv('PORT', 25575))
password = getenv('PASSWORD')

with Client(host, port, passwd=password) as client:
    print(client.run('ShowPlayers', enforce_id=False))
    # print(client.run('Save', enforce_id=False))
