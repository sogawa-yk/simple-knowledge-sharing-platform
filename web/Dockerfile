# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV DATABASE_HOST qiita-sample-db
ENV DATABASE_USER root
ENV DATABASE_PASSWORD password
ENV DATABASE_NAME flask_app

# 必要なファイルをコンテナにコピー
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY custom_markdown.py custom_markdown.py
COPY templates/ templates/
COPY static/ static/
COPY uploads/ uploads/

# 依存関係をインストール
RUN pip install -r requirements.txt

# アップロードディレクトリのパーミッションを設定
RUN chmod -R 777 /app/uploads

# コンテナの起動時に実行されるコマンド
CMD ["python", "app.py"]
