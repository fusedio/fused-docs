import os
from enum import Enum
from typing import Optional

from fused._options import ShowOptions
from fused._options import options as OPTIONS


class Environment(str, Enum):
    AZURE = "azure"
    COCALC = "cocalc"
    COLAB = "colab"
    DATABRICKS = "databricks"
    KAGGLE = "kaggle"
    NTERACT = "nteract"
    OTHER_IPYTHON = "other_ipython"
    TERMINAL = "terminal"
    UNKNOWN = "unknown"
    VSCODE = "vscode"


def deduce_environment() -> Environment:
    # https://github.com/plotly/plotly.py/blob/fc3ef002c7a7898b9244b1549757a64e8df266dd/packages/python/plotly/plotly/io/_renderers.py#L469

    try:
        import IPython

        ipython = IPython.get_ipython()
        try:
            import google.colab  # noqa: F401

            return Environment.COLAB
        except ImportError:
            pass

        # Check if we're running in a Kaggle notebook
        if os.path.exists("/kaggle/input"):
            return Environment.KAGGLE

        # Check if we're running in an Azure Notebook
        if "AZURE_NOTEBOOKS_HOST" in os.environ:
            return Environment.AZURE

        # Check if we're running in VSCode
        if "VSCODE_PID" in os.environ:
            return Environment.VSCODE

        # Check if we're running in nteract
        if "NTERACT_EXE" in os.environ:
            return Environment.NTERACT

        # Check if we're running in CoCalc
        if "COCALC_PROJECT_ID" in os.environ:
            return Environment.COCALC

        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            return Environment.DATABRICKS

        if ipython.__class__.__name__ == "TerminalInteractiveShell":
            return Environment.TERMINAL

        return Environment.OTHER_IPYTHON
    except ImportError:
        pass

    return Environment.UNKNOWN


def infer_display_method(open_browser: Optional[bool], show_widget: Optional[bool]):
    # Passed-in options have highest precedence
    if open_browser is not None or show_widget is not None:
        return ShowOptions(open_browser=open_browser, show_widget=show_widget)

    if OPTIONS.show.open_browser is not None or OPTIONS.show.show_widget is not None:
        return OPTIONS.show

    if ENVIRONMENT in [
        Environment.TERMINAL,
        Environment.UNKNOWN,
    ]:
        return ShowOptions(open_browser=True, show_widget=False)
    else:
        return ShowOptions(open_browser=False, show_widget=True)


def is_pyodide():
    # https://pyodide.org/en/stable/usage/faq.html#how-to-detect-that-code-is-run-with-pyodide
    import sys

    return "pyodide" in sys.modules


ENVIRONMENT = deduce_environment()
