"""
Obsidianノート検索用Streamlitアプリケーション
"""

import os
import streamlit as st
from obsidian_search_app.searcher import ObsidianSearcher


def run_app(index_path=None, map_path=None):
    """
    Streamlitアプリを実行する
    
    Args:
        index_path: インデックスファイルのパス
        map_path: マッピングファイルのパス
    """
    if index_path is None:
        index_path = os.path.join(os.getcwd(), 'obsidian_notes_index.npy')
    if map_path is None:
        map_path = os.path.join(os.getcwd(), 'file_content_map.json')
    
    searcher = ObsidianSearcher(index_path, map_path)
    
    st.title("Obsidianノート検索アプリ")
    query = st.text_input("検索クエリを入力してください")
    
    if st.button("検索"):
        if query:
            results = searcher.search(query)
            st.write("検索結果:")
            for file_path, content, score in results:
                # ファイルパスをObsidianのURIスキームで表示
                obsidian_uri = f"obsidian://open?vault=Obsidian&file={file_path.replace('../Obsidian/', '').replace('.md', '')}"
                st.write(f"[{file_path}]({obsidian_uri})")
                st.write(f"スコア: {score:.4f}")
                st.write(content[:200])  # 最初の200文字を表示
                st.write("---")
        else:
            st.warning("検索クエリを入力してください")


# スクリプトとして直接実行された場合
if __name__ == "__main__":
    run_app()
