import sys
from os.path import join, dirname

c = get_config()  # noqa

here = dirname(__file__)

c.JupyterHub.authenticator_class = 'nullauthenticator.NullAuthenticator'
c.JupyterHub.services = [
    {
        'name': 'login',
        'admin': True,
        'command': [sys.executable, join(here, 'login-service.py')],
        'url': 'http://127.0.0.1:4202',
    }
]

# use Docker for spawning
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.remove_containers = True
