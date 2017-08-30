"""An example service that creates users via the API

without needing the Hub to support login of any kind.
"""
from getpass import getuser
import json
import os
from urllib.parse import urlparse

from tornado.ioloop import IOLoop
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.httpserver import HTTPServer
from tornado.log import app_log
from tornado import web
from tornado.web import RequestHandler, Application

from jupyterhub.utils import url_path_join


def api_request(path, **kwargs):
    """Make an API request to the Hub

    to reduce boilerplate repetition.
    """

    url = url_path_join(os.environ['JUPYTERHUB_API_URL'], path)
    client = AsyncHTTPClient()
    headers = {
        'Authorization': 'token %s' % os.environ['JUPYTERHUB_API_TOKEN'],
    }
    if kwargs.get('method') == 'POST':
        kwargs.setdefault('body', '')
    req = HTTPRequest(url, headers=headers, **kwargs)
    return client.fetch(req)


async def delete_user(name):
    """Stop a user's server and delete the user"""
    app_log.info("Deleting user %s", name)
    await api_request('users/{}/server'.format(name), method='DELETE')
    await api_request('users/{}'.format(name), method='DELETE')


class LoginHandler(RequestHandler):
    def get(self):
        # GET renders the form
        self.render('login.html')

    async def post(self):
        # DEF is called on form submission
        name = self.get_argument('username')
        # create the user
        try:
            resp = await api_request('users/{}'.format(name), method='POST')
        except HTTPError as e:
            raise web.HTTPError(400, str(e))
        # spawn the user's server
        spawn_future = api_request('users/{}/server'.format(name), method='POST')
        # request a token for the user
        resp = await api_request(
            'authorizations/token',
            method='POST',
            body=json.dumps({
                'username': name
            }),
        )
        reply = json.loads(resp.body.decode('utf8'))
        token = reply['token']
        # wait for the server to start
        reply = await spawn_future
        # schedule user for deletion after five minutes!
        IOLoop.current().call_later(300, delete_user, name)
        # redirec to /user/:name/?token=...
        url = url_concat(
            url_path_join(os.environ['JUPYTERHUB_BASE_URL'], 'user', name, '/'),
            {'token': token},
        )
        self.redirect(url)


def main():
    app = Application([
        ('.*', LoginHandler),
    ])

    http_server = HTTPServer(app)
    url = urlparse(os.environ['JUPYTERHUB_SERVICE_URL'])

    http_server.listen(url.port, url.hostname)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
