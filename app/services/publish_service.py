import subprocess
import re
from dataclasses import dataclass
from pathlib import Path
from app.core.settings import ROOT_DIR, ARTICLES_DIR
from app.services.file_service import FileService

@dataclass
class PublishResult:
    result: bool
    slug: str

class PublishService:
    def __init__(self, root_dir: Path = ROOT_DIR) -> None:
        self.file_service = FileService()
        self.root_dir = root_dir

    def publish_article(self, slug: str) -> PublishResult:
        # 対象ファイルを検索
        md_files = list(ARTICLES_DIR.glob(f"*{slug}*.md"))
        if not md_files:
            raise FileNotFoundError(f"記事が見つかりません: slug={slug}")

        article_path = md_files[0]

        # Frontmatter 書き換え
        with open(article_path, "r") as file:
            content = file.read()
        
        new_content = re.sub(r"published:\s*false", "published: true", content)
        match_title = re.search(r'title:\s*"(.+?)"', content)

        if match_title:
            article_title = match_title.group(1)
        else:
            article_title = "Untitled"

        with open(article_path, "w") as file:
            file.write(new_content)
        
        article_slug: str = self.file_service.get_article_slug(article_path=article_path)

        # Git 連携
        try:
            subprocess.run(["git", "add", "."], cwd=str(self.root_dir), check=True, capture_output=True, text=True)
            subprocess.run(["git", "commit", "-m", f"publish {article_title}"], cwd=str(self.root_dir), check=True, capture_output=True, text=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=str(self.root_dir), check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"git_result: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
            return PublishResult(False, article_slug)

        return PublishResult(True, article_slug)
