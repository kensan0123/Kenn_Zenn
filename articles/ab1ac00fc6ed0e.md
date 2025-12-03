---
title: "個人開発を始めました！Zenn CLIをFastAPIでラップしてLLMと接続してみます"
emoji: "🚀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Python"]
published: true
---

## 導入
個人開発を進める際には、CLIツールをどうAPI化して他のサービスと連携させるかが重要なテーマです。本記事では、Zenn CLIをFastAPIでラップして、LLMと接続する実装を紹介します。Zenn CLIは記事の作成・公開を自動化できる強力なツールですが、HTTP経由で操作できれば外部アプリケーションやエディタの拡張機能と容易に連携できます。実装のゴールは以下のとおりです。
- Zenn CLIのコマンドをREST APIとして公開
- LLMを介して記事の下書き・リサーチ・要約を自動生成
- ローカル環境で開発・検証し、後にデプロイ可能な設計

参考URL: https://github.com/kensan0123/Kenn_Zenn

## 背景
近年、LLMを活用したアプリケーションは急速に拡大しています。Zennは技術記事の作成・公開を促進するCLIツールであり、これをHTTP APIとして公開することで、エディタ拡張・自動化スクリプト・CI/CDパイプラインなどと組み合わせやすくなります。本稿では FastAPI を使って Zenn CLI の操作をRESTエンドポイントとして公開し、LLMとの連携を実現する設計を解説します。参考にしたリポジトリは Kenn_Zenn です。

## 手順
以下の手順で実装します。

### 1. 環境準備
- Python 3.9 以降
- 仮想環境の作成と依存関係のインストール
- Zenn CLI の事前インストールと認証設定

インストール例:
- python -m venv venv
- source venv/bin/activate
- pip install fastapi uvicorn openai pydantic
- zenn --version  # Zenn CLI が利用可能であることを確認

### 2. アーキテクチャの設計
- FastAPI アプリが受け取るエンドポイント
  - /zenn/run: Zenn CLI の任意コマンドを実行するラッパー
  - /zenn/llm: Zenn 出力に対して LL M で要約・下書きを生成するエンドポイント
- データモデル
  - ZennCommand: command 文字列、args 文字列リスト
- 実行の安全性
  - 実行可能なコマンドのホワイトリスト化
  - 入力値の検証とログ出力

### 3. FastAPI アプリの雛形
<pre><code class='language-python'>from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI()

class ZennCommand(BaseModel):
    command: str
    args: List[str] = []

async def run_command(cmd):
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return {'stdout': out.decode(), 'stderr': err.decode(), 'rc': proc.returncode}

@app.post('/zenn/run')
async def zenn_run(payload: ZennCommand):
    cmd = ['zenn', payload.command] + payload.args
    result = await run_command(cmd)
    return result
</code></pre>

### 4. Zenn CLI 呼び出しの実装
<pre><code class='language-python'>import subprocess
from typing import List
import asyncio

async def run_command(cmd: List[str]):
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return {'stdout': out.decode(), 'stderr': err.decode(), 'rc': proc.returncode}

# 実運用時には、ホワイトリストの検証を追加して安全性を確保します
</code></pre>

### 5. LLM 連携の実装
<pre><code class='language-python'>import openai

def ask_llm(prompt, api_key=None, model='gpt-4'):
    if api_key:
        openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return resp.choices[0].message['content'].strip()
</code></pre>

### 6. 結合テストとデバッグ
- まずローカルで FastAPI サーバを起動します
  - uvicorn main:app --reload --port 8000
- Zenn CLI の動作確認
- LLM 連携のレスポンス検証

### 7. 運用とデプロイ
- セキュリティ対策: API キー管理、CORS、ロギング、監視
- 実行環境の分離: Docker などによるコンテナ化
- コンテンツ監査: LLM 偽情報対策と出力の検証

### 8. 使い方の例
- 開発時のワークフローとして、エディタから /zenn/run に対してボタン操作で Zenn CLI を呼び出す
- LLM 結果を元に下書きを編集して Zenn に投稿するまでの一連の流れを自動化可能

## 参考
- Kenn_Zenn: https://github.com/kensan0123/Kenn_Zenn

## まとめ
本稿では、Zenn CLIをFastAPIでラップし、LLMと接続する基本パターンを紹介しました。セキュリティや運用の観点を踏まえ、ローカル環境での検証を経て、安全なAPIを構築することが重要です。今後は認証機構の強化や、バッチ処理・非同期処理の拡張、CI/CD 連携の検討を進めたいと考えています。

この記事はAIによって作成されました。
