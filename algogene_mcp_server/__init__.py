import sys

from . import config as _config

sys.modules.setdefault("config", _config)

from . import utils as _utils
from . import tools as _tools

sys.modules.setdefault("utils", _utils)
sys.modules.setdefault("tools", _tools)
