from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from fused._global_api import get_api

if TYPE_CHECKING:
    from fused.api import FusedAPI

# Pydantic methods to remove in __dir__
PYDANTIC_METHODS = {
    "Config",
    "construct",
    "copy",
    "from_orm",
    "json",
    "parse_file",
    "parse_obj",
    "schema",
    "schema_json",
    "update_forward_refs",
    "validate",
    "model_config",
    "model_construct",
    "model_copy",
    "model_dump",
    "model_dump_json",
    "model_extra",
    "model_fields",
    "model_fields_set",
    "model_json_schema",
    "model_parametrized_name",
    "model_post_init",
    "model_rebuild",
    "model_validate",
    "model_validate_json",
    "model_validate_strings",
    "parse_raw",
    "model_computed_fields",
}


class FusedBaseModel(BaseModel):
    @property
    def _api(self) -> FusedAPI:
        # Note that this does not import the FusedAPI class for circular import reasons
        # We assume that the API has already been instantiated before a model is created
        return get_api()

    def __dir__(self) -> List[str]:
        """Provide method name lookup and completion. Only provide 'public'
        methods.
        """
        # This enables autocompletion.
        normal_dir = {
            name
            for name in dir(type(self))
            if not name.startswith("_") and name not in PYDANTIC_METHODS
        }
        pydantic_fields = set(self.model_fields.keys())

        return sorted(normal_dir | pydantic_fields)

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


UserMetadataType = Optional[Dict[str, Any]]
