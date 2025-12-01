import os
from pathlib import Path

# Base path for Zenn workspace (can be overridden via env ZENN_DIR)
ZENN_DIR = Path(os.getenv("ZENN_DIR", "/zenn")).resolve()
ARTICLES_DIR = ZENN_DIR / "articles"
