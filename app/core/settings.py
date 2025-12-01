import os
from pathlib import Path

from dotenv import load_dotenv

# Base directory of this repository (app/core sits two levels below root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables from project .env when running outside Docker
load_dotenv(PROJECT_ROOT / ".env", override=False)


def resolve_path(path_value: str | None, default: Path) -> Path:
    """Resolve env paths relative to project root to keep subprocess cwd stable."""
    if not path_value:
        return default

    path = Path(path_value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()

def create_netrc():
    home = os.path.expanduser("~")
    netrc_path = os.path.join(home, ".netrc")

    content = "\n".join(
        [
            "machine github.com",
            f"login {os.getenv('GITHUB_USER', '')}",
            f"password {os.getenv('GITHUB_PAT', '')}",
            "",
        ]
    )

    with open(netrc_path, "w") as f:
        f.write(content)

    os.chmod(netrc_path, 0o600)


# Base path for git/Zenn workspace (can be overridden via env ROOT_DIR/ZENN_DIR)
ROOT_DIR = resolve_path(os.getenv("ROOT_DIR"), PROJECT_ROOT)
ZENN_DIR = resolve_path(os.getenv("ZENN_DIR"), ROOT_DIR / "zenn")
ARTICLES_DIR = ROOT_DIR / "articles"
