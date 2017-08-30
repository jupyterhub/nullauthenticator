# NullAuthenticator

Null Authenticator for JupyterHub instances that should have no login mechanism,
such as those that exclusively allow access via API token.

Enable null authenticator:

```python
c.JupyterHub.authenticator_class = 'nullauthenticator.NullAuthenticator'
```
