---
sidebar_label: _auth
title: fused._auth
---

## Credentials Objects

```python showLineNumbers
class Credentials(BaseModel)
```

A dataclass representation of OAuth2 credentials

## MaybeInitializedCredentials Objects

```python showLineNumbers
class MaybeInitializedCredentials()
```

OAuth2 credentials that may or may not have been initialized.

## initialize

```python showLineNumbers
def initialize() -> None
```

Force initialization of credentials.

## credentials

```python showLineNumbers
@property
def credentials() -> Credentials
```

Retrieve valid credentials, initializing them or authenticating from scratch if needed.

## \_authorization\_header

```python showLineNumbers
@property
def _authorization_header()
```

Access the Authorization HTTP header of these credentials.

## CREDENTIALS

Global credentials.

## logout

```python showLineNumbers
def logout()
```

Open the user's browser to the Auth0 logout page.

## get\_code\_challenge

```python showLineNumbers
def get_code_challenge(code_verifier: str) -> str
```

Take an input string and hash it to generate a challenge string

Refer to https://auth0.com/docs/get-started/authentication-and-authorization-flow/call-your-api-using-the-authorization-code-flow-with-pkce

## handle\_redirect

```python showLineNumbers
def handle_redirect(authorize_url: str) -> str
```

Open the authorization url and intercept its redirect

The redirection from the `/authorize` endpoint includes a code that can be used
against the `/oauth/token` endpoint to fetch a refresh and access token.

## refresh\_token

```python showLineNumbers
def refresh_token(refresh_token: str)
```

Generate a new access_token using a refresh token
