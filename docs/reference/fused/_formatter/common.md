---
sidebar_label: common
title: fused._formatter.common
---

#### load\_static\_files

```python
@lru_cache(None)
def load_static_files()
```

Lazily load the resource files into memory the first time they are needed

#### copyable\_text

```python
def copyable_text(text: Optional[str], *, show_text: bool = True) -> str
```

Returns an HTML fragment for a copyable text block

