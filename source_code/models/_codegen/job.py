import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from fused.models.base import FusedBaseModel

from .udf import structure_params


class CustomJobConfig(FusedBaseModel):
    name: Optional[str] = None
    steps: List[Dict[str, Any]] = []  # Support steps of flexible structure
    metadata: Optional[Dict[str, Any]] = None
    _validate_version: bool = True


class MetaJson(FusedBaseModel):
    job_config: CustomJobConfig


def _structure_udf_file_name(udf_name):
    return f"udf_{udf_name}.py"


def create_directory_and_zip(
    path: str, how: Literal["zip", "local"], files: Dict, overwrite: bool = False
):
    def _create_files_in_directory(path_obj, files, tmpdir=False):
        # Create dir
        if not path_obj.exists():
            path_obj.mkdir()

        # Write files
        for filename, file_contents in files.items():
            file_path = path_obj / filename
            with open(file_path, "w") as file:
                if isinstance(file_contents, Dict):
                    # Prettify JSON files
                    file_contents = json.dumps(
                        json.loads(json.dumps(file_contents)), indent=4, sort_keys=True
                    )
                file.write(file_contents)
        return path_obj

    def _write_files_to_zip(path_obj, path_obj_with_files):
        with zipfile.ZipFile(path_obj, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(path_obj_with_files):
                for file in files:
                    source_filepath = Path(root) / file
                    relative_path = os.path.relpath(
                        source_filepath, path_obj_with_files
                    )

                    zipf.write(source_filepath, relative_path)

    if isinstance(path, (str, Path)):
        path_obj = Path(path)
        base_name = path_obj.stem

        if path_obj.exists():
            if not overwrite:
                raise FileExistsError(f"Object {path} already exists.")
            else:
                if path_obj.is_dir():
                    shutil.rmtree(path_obj)
                elif path_obj.is_file():
                    path_obj.unlink()
    else:
        path_obj = path
        base_name = "udf"

    if how == "zip":
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path_obj = Path(tmpdir) / base_name
            path_obj_with_files = _create_files_in_directory(
                tmp_path_obj, files, tmpdir=True
            )
            _write_files_to_zip(path_obj, path_obj_with_files)
    elif how == "local":
        if isinstance(path_obj, Path) and path_obj.suffix:
            # TODO: Warning, not error
            raise ValueError(
                "To export with `how='local'`, path must be a directory, not a file."
            )

        _create_files_in_directory(path_obj, files)
    else:
        raise NotImplementedError(f"{how=} is not implemented")


def generate_readme(job):
    """Structure text for README.md."""
    job_names = [f"job_{step.udf.name}" for step in job.steps]

    jobs = []
    for step in job.steps:
        jobs.append(
            f"job_{step.udf.name} = {step.udf.name}({structure_params(step._generate_job_params())})"
        )

    str_udf_imports = "\n".join(
        [f"from udf_{step.udf.name} import {step.udf.name}" for step in job.steps]
    )
    str_run_local = "job.run_local(file_id=0, chunk_id=0)"
    str_run_remote = "job.run_remote(output_table='output_table_name')"
    str_job = "\n".join(jobs)
    str_multijob = f"job = fused.experimental.job([{', '.join(job_names)}])"
    src = f"""
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
{str_udf_imports}

# Instantiate individual jobs
{str_job}

# Instantiate multi-step job
{str_multijob}

# Run locally
{str_run_local}

# Run remotely
{str_run_remote}
```
"""
    return src


def generate_meta_json(job):
    """Structure json for `meta.json`."""
    job_config = job.model_dump()
    steps = []
    for step in job_config["steps"]:
        step["udf"]["source"] = _structure_udf_file_name(step["udf"]["name"])
        step["udf"]["metadata"] = {
            "fused:slug": step["udf"]["name"],  # METADATA_FUSED_SLUG
            "fused:name": step["udf"]["name"],  # METADATA_FIELD_NAME
        }
        del step["udf"]["code"]
        for header in step["udf"]["headers"]:
            # If there's no source file, introduce source file name
            if not header["source_file"]:
                header["source_file"] = header["module_name"] + ".py"  # virtual

            # Set relative path to sibling file.
            if not header["source_file"].startswith(("http", "https", "www")):
                header["source_file"] = header["module_name"] + ".py"
            # Remove `source_code` field.
            del header["source_code"]
        steps.append(step)

    job_config["steps"] = steps

    # Structure JSON
    return MetaJson(job_config=job_config).model_dump_json()
