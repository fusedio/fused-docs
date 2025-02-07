from typing import List

from fused._formatter.udf import fused_registry_repr


class Registry(dict):
    def _repr_html_(self):
        return fused_registry_repr(self)

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __dir__(self) -> List[str]:
        """Provide method name lookup and completion. Only provide 'public'
        methods.
        """
        # This enables autocompletion
        extra_attrs = set(self.keys())
        normal_dir = {name for name in dir(type(self)) if not name.startswith("_")}

        return sorted(normal_dir | extra_attrs)
