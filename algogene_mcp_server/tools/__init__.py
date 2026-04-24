# Original version:
# This file was empty.

import builtins
from typing import Any, Dict, List


# Compatibility shim for tool modules that use typing annotations without
# importing the names they reference.
builtins.Any = Any
builtins.Dict = Dict
builtins.List = List
