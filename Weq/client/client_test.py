import socket
import json
from keydistribution import KeyDistribution
from client import Client

private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAp5vNnufEgtA/JywVlDnIAQpI4+o7L3SlpurxJbfO9cpUKsyx\n3/6ITSjAVojvJdrhzV+zVWBdI8rlP0mln4Tke59eNCHWhK0Cs7Zp3es0z2rcYSIY\nA84CR8Uqc3b/ZGAHjq5iGZN2HHQjB+FHFVHkD59bayNuOoqxRd8oNz/mt4pUtWSt\nQLnWdvsO9pXEEc7ULE4jSqT/d64j8pmgMXkUw5tpW1cIqoLU9J0uDje9HK0FP783\n2pWZROEEWJUYL5NTVN9OL0getDkpfX+7F017HBAjPFr+l+4ESciPJK+nwiQ/PVs0\nebvP+Gvyzt0UCYTsG3WBughgB31oYbavJy8OOwIDAQABAoIBABSUIhJdFXkUNXTL\nSlj5IS/TgfCNzTd95GrSlMoTP9NYxK2+lSZR241RsA/P30DwF2I+WkfkvXrMCgqT\nscScrerpvci70NlYXqkO//+RxdmjnqxEYdtxu0Dxmc00cpXx3muryHqoasuCjNyG\nUdJxzAUJBVHptzpz1eEkzYy/CUZGgEON9R5X5OMQTYyNzyezqn4xn/ev+N43DL2s\nPuc9Y3UAgJY/8ZAin7wTphP8R7NnRd6h8nm8JOoXj5QqqHTUcG4Dsk8160K1Gsbo\nDLyn/qGuZuhuAebuGpKdjT11JgsRLKQKUCPSjDchzJX/EXJpbg0G/lxXar4E0m3H\nDGPtzTkCgYEAxSvMtZx9SeK+o/+Y/kLshV79ZZp7EfdnZ9gMjUXfanSc4664g6EP\nsmQ+7lvapoYCaLN+h2BfQtaZpU2io5eo+GnjaMGvLDXtMmSihDsorDb8FsVJRTcn\nVvUU0o2jSCYBoYjwosYWGav3iLcMyu5285Wtrk799b9NFyKO7MHe1FkCgYEA2Z36\n5Ay/ptf+/sg9WcOIHy3m93RSULHMkPinDGoiq64bT93ykK3AtE1qw1vxRuTWQMvT\nNdMRZUPWmOg6tBzThQK+7Z+afb5wsjuoz3BAYfhnp+csHr4rRrhkA0BCpmQ+v/Z3\nQfP0nL7UWImgjIGtkoJHjRB4YZ1KweKCsolitLMCgYBjvURQmljGh2zoiONbu37p\n+KM2Qm7/J6enYCL5U98wesziX//2lgLautsauFxi4GdXj3TyBk4qAWS3ug4LsyxG\nfUoMM+3o716Nn1qWiVaJx0a+Pg5SdRPxaQifegae+Jram+sebBXB5rvQ7MgL35VM\nouq4wjy1k4/rpA+otGmEAQKBgQCqcvcEkIe8ownzfduv51tDMKzrvYyL7/eOxXPy\nYV9uoRx7XhiUAcQidVDeW7GMGclHT17LldrWOmBnu93fHYT/dbseXBihzPxwXhJH\nCGElW2+1L3h7S/CRn/OWKEsMERClQuL+IZrC+yVPg9zgsOHHE4v/jZr8ujrHyicc\nuEc7yQKBgQDExbgSVC8tFfKIyibCsMGR/KncQfNY+Ess73o30kzhEusdxI7rZxpr\nWB+3Q+cjRm8AOjglZwG8FqZwWENFhOmFX+7r4Xn1oIZtwMFy/Ib5ila+n7XEunpv\nhnaJBZNwVorp3PgMvzYrs+rHlsgW8KLtg2X7rz+uhvMQr7ytcMBWGQ==\n-----END RSA PRIVATE KEY-----'

kd = KeyDistribution('10.21.184.19', 8000, private_key)
kd.get_session_key_from_server('astra', 'astra')
kd.send_session_key_to_peer('127.0.0.1', 8888)

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('10.21.237.247', 16666))
# client.send(b'getPubkey\r\n\r\n{"user":"astra","sendto":"astra"}')
# print(client.recv(1024))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888))
data = json.dumps({'action': 'chat', 'ip': '127.0.0.1', 'port': 8000})
client.send(data.encode('utf-8'))
client.close()

a = Client('10.21.184.19', 8000)
a.session_key = kd.session_key
a.chat('127.0.0.1', 8888)