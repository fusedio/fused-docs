from typing import List

from fused._formatter.udf import fused_registry_repr


class UdfRegistry(dict):
    def _repr_html_(self):
        return fused_registry_repr(self)

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # IPython's _repr_html_ requires AttributeError instead of KeyError.
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __dir__(self) -> List[str]:
        """Provide method name lookup and completion."""
        extra_attrs = set(self.keys())
        return sorted(extra_attrs)
