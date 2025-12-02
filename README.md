## Kenn_Zenn

FastAPI service that wraps the Zenn CLI to generate and publish articles.

## Quick start

1) Create a Zenn account: https://zenn.dev  
2) Clone this repo:

```bash
git clone https://github.com/kensan0123/Kenn_Zenn.git
cd Kenn_Zenn
```

3) Copy `.envexample` to `.env` and fill in values:

```bash
cp .envexample .env
```

4) Start the app with Docker:

```bash
docker compose up
```

## API

- `POST /generate` – creates an article and returns the generated slug. Omit `slug` to let Zenn generate it.

```json
{
  "title": "string",
  "emoji": "string",
  "content": "string",
  "slug": "string (optional)"
}
```

- `POST /publish` – publishes the article for the given slug.

```json
{
  "slug": "string"
}
```
