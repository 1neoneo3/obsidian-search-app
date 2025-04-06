# Obsidianノート検索アプリ

Obsidianノートを意味検索できるアプリケーションです。自然言語処理を活用して、キーワードだけでなく意味的に関連するノートを検索できます。

## 機能

- Obsidianノートの意味検索
- 検索結果からObsidianへの直接リンク
- 類似度スコアの表示
- 検索結果のプレビュー

## 必要条件

- Python 3.11
- 以下の依存パッケージ:
  - numpy>=1.20.0
  - sentence-transformers>=3.1.1
  - streamlit==1.32.2
  - torch>=2.6.0
  - transformers==4.38.2
  - webdriver-manager>=4.0.0

## インストール方法

1. リポジトリをクローン:
```bash
git clone https://github.com/yourusername/obsidian-search-app.git
cd obsidian-search-app
```

2. 依存パッケージのインストール:
```bash
uv sync
```

または:
```bash
pip install -e .
```

## 使用方法

### インデックスの作成

最初に、Obsidianノートのインデックスを作成する必要があります:

```bash
python -m obsidian_search_app.cli index --directory /Users/io/Documents/Obsidian
```

※ Obsidianノートのディレクトリを適切に指定してください。

### 検索アプリの起動

インデックスを作成した後、検索アプリを起動できます:

```bash
streamlit run run_app.py
```

ブラウザが自動的に開き、検索インターフェースが表示されます。

## プロジェクト構成

```
obsidian_search_app/
├── .gitignore
├── README.md
├── pyproject.toml
├── run_app.py                   # Streamlitアプリ単独実行ファイル
└── src/
    └── obsidian_search_app/     # パッケージディレクトリ
        ├── __init__.py
        ├── app.py               # Streamlitアプリ
        ├── cli.py               # コマンドラインインターフェース
        ├── indexer.py           # インデックス作成モジュール
        └── searcher.py          # 検索モジュール
```

## 注意点

- Python 3.11で動作確認済みです
- 依存関係のバージョンは厳密に守る必要があります
- 初回実行時にはインデックス作成が必要です
- インデックスファイルは大きくなる可能性があるため、`.gitignore`でデフォルトで除外しています
