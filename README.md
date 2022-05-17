# NullAuthenticator

[![PyPI](https://img.shields.io/pypi/v/nullauthenticator.svg)](https://pypi.org/project/nullauthenticator/)


Null Authenticator for JupyterHub instances that should have no login mechanism,
such as those that exclusively allow access via API token.

## Installation

As prerequisites, Python 3.4+ and JupyterHub 0.8.0+ are required to use Null
Authenticator.

To install `nullauthenticator`, enter in a terminal:

```
python3 -m pip install nullauthenticator
```

## Usage

Enable null authenticator in `jupyterhub_config.py`:

```python
c.JupyterHub.authenticator_class = 'nullauthenticator.NullAuthenticator'
```

## Example

The `examples` directory of this repo demonstrates a [token-only example](./examples/token-only/README.md)
with Null Authenticator which uses external user creation and authentication.
