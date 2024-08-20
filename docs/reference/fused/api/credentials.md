---
sidebar_label: credentials
title: fused.api.credentials
---

## NotebookCredentials Objects

```python showLineNumbers
class NotebookCredentials()
```

To use this credentials helper, run the following and it will guide you to create a FusedAPI object.

```py
credentials = NotebookCredentials()
```

## logout

```python showLineNumbers
def logout()
```

Log out the current user.

This deletes the credentials saved to disk and resets the global Fused API.

## access\_token

```python showLineNumbers
def access_token() -> str
```

Get an access token for the Fused service.
