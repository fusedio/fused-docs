---
sidebar_label: _auth
title: fused._auth
---

## Credentials Objects

```python
class Credentials(BaseModel)
```

A dataclass representation of OAuth2 credentials

## MaybeInitializedCredentials Objects

```python
class MaybeInitializedCredentials()
```

OAuth2 credentials that may or may not have been initialized.

#### initialize

```python
def initialize() -> None
```

Force initialization of credentials.

#### credentials

```python
@property
def credentials() -> Credentials
```

Retrieve valid credentials, initializing them or authenticating from scratch if needed.

#### CREDENTIALS

Global credentials.

#### logout

```python
def logout()
```

Open the user&#x27;s browser to the Auth0 logout page.

#### get\_code\_challenge

```python
def get_code_challenge(code_verifier: str) -> str
```

Take an input string and hash it to generate a challenge string

Refer to https://auth0.com/docs/get-started/authentication-and-authorization-flow/call-your-api-using-the-authorization-code-flow-with-pkce

#### handle\_redirect

```python
def handle_redirect(authorize_url: str) -> str
```

Open the authorization url and intercept its redirect

The redirection from the `/authorize` endpoint includes a code that can be used
against the `/oauth/token` endpoint to fetch a refresh and access token.

#### refresh\_token

```python
def refresh_token(refresh_token: str)
```

Generate a new access_token using a refresh token

