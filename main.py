
from rcon.source import Client

with Client(host, rcon_port, passwd=password) as client:
    print(client.run('ShowPlayers', enforce_id=False))
    # print(client.run('Save', enforce_id=False))
