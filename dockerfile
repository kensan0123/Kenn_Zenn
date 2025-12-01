FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ZENN_DIR=/zenn

WORKDIR /app

ARG user_name
ARG user_email

# Install Node.js/npm for Zenn CLI and git for publish step
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates git nodejs npm \
    && npm install -g zenn-cli \
    && rm -rf /var/lib/apt/lists/*

# Create .netrc for GitHub auth
RUN touch /root/.netrc && chmod 600 /root/.netrc

# Apply git config
RUN : "${user_name:?Set user_name build-arg}" \
    && : "${user_email:?Set user_email build-arg}" \
    && git config --global user.name "$user_name" \
    && git config --global user.email "$user_email"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 9000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
