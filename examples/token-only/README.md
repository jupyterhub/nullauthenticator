# token-authenticated example

This is an example of external user creation and authentication.
Login via the hub is unavailable.
Instead, a separate service running at `/services/login` is run with admin permissions.
This has a simple form where a user can input a username.

When the form is submitted, the service performs the following actions:

1. create a user with the requested name
2. spawn a server for that user
3. request an API token for that user
4. redirect the browser to /user/:name/?token=...