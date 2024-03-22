---
sidebar_label: migrations
title: fused.models.migrations
---

#### migration

```python
def migration(cls, from_version)
```

Decorator for adding a migration function to an object class. Use this

decorator on any function or method that should be used for migrating an
object from one version to another. This is an equivalent alternative to the
versionedobject.object.add_migration function.

**Arguments**:

- `cls`: Class object to add migration to
- `from_version`: Version to migrate from. If you are migrating an object that        previously had no version number, use &#x27;None&#x27; here.
- `to_version`: Version to migrate to

