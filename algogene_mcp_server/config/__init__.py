import os
from pathlib import Path


def _load_dotenv():
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

BASE_URL = os.getenv("ALGOGENE_BASE_URL", "https://algogene.com/rest")

ALGOGENE_USER = os.getenv("ALGOGENE_USER", "")
ALGOGENE_API_KEY = os.getenv("ALGOGENE_API_KEY", "")
