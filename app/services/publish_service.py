import subprocess
import re
from dataclasses import dataclass
from pathlib import Path
from app.core.settings import ZENN_DIR, ARTICLES_DIR
from app.services.file_service import FileService

@dataclass
class PublishResult:
    result: bool
    slug: str

class PublishService:
    def __init__(self) -> None:
        self.file_service = FileService()

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
        subprocess.run(["git", "add", "."], cwd=str(ZENN_DIR), check=True)
        subprocess.run(["git", "commit", "-m", f"publish {article_title}"], cwd=str(ZENN_DIR), check=True)
        subprocess.run(["git", "push"], cwd=str(ZENN_DIR), check=True)

        return PublishResult(True, article_slug)
