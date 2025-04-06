"""
Obsidianノート検索アプリのコマンドラインインターフェース
"""

import os
import argparse
from obsidian_search_app.indexer import index_notes
from obsidian_search_app.app import run_app


def main():
    """コマンドラインエントリーポイント"""
    parser = argparse.ArgumentParser(description="Obsidianノート検索アプリ")
    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")
    
    # インデックス作成コマンド
    index_parser = subparsers.add_parser("index", help="Obsidianノートのインデックスを作成")
    index_parser.add_argument(
        "--directory", "-d", 
        default="/Users/io/Documents/Obsidian", 
        help="Obsidianノートのディレクトリ (デフォルト: /Users/io/Documents/Obsidian)"
    )
    index_parser.add_argument(
        "--output", "-o", 
        default=os.getcwd(),
        help="インデックスの出力先ディレクトリ (デフォルト: カレントディレクトリ)"
    )
    
    # 検索アプリ起動コマンド
    app_parser = subparsers.add_parser("search", help="検索アプリを起動")
    app_parser.add_argument(
        "--index", "-i", 
        default=None,
        help="インデックスファイルのパス (デフォルト: カレントディレクトリの'obsidian_notes_index.npy')"
    )
    app_parser.add_argument(
        "--map", "-m", 
        default=None,
        help="マッピングファイルのパス (デフォルト: カレントディレクトリの'file_content_map.json')"
    )
    
    args = parser.parse_args()
    
    if args.command == "index":
        print(f"Obsidianノートのインデックスを作成中... ディレクトリ: {args.directory}")
        index_path, map_path = index_notes(args.directory, args.output)
        print(f"インデックスを作成しました: {index_path}")
        print(f"マッピングファイルを作成しました: {map_path}")
    
    elif args.command == "search":
        print("検索アプリを起動中...")
        run_app(args.index, args.map)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
