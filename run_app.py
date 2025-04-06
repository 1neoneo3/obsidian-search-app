"""
Obsidianノート検索アプリの実行スクリプト
"""

import os
import streamlit as st
import numpy as np
import json
from sentence_transformers import SentenceTransformer, util


class ObsidianSearcher:
    """Obsidianノート検索クラス"""
    
    def __init__(self, index_path, map_path):
        """
        初期化
        
        Args:
            index_path: 埋め込みベクトルのインデックスファイルパス
            map_path: ファイルパスと内容のマッピングファイルパス
        """
        self.embeddings = np.load(index_path)
        with open(map_path, 'r', encoding='utf-8') as f:
            self.file_content_map = json.load(f)
        
        # モデルの読み込み
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def search(self, query, top_k=5):
        """
        クエリに基づいてノートを検索する
        
        Args:
            query: 検索クエリ
            top_k: 返す結果の数
            
        Returns:
            検索結果のリスト [(ファイルパス, 内容, スコア), ...]
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=top_k)
        hits = hits[0]  # semantic_searchの結果はリストのリストとして返される
        
        results = []
        for hit in hits:
            file_path = list(self.file_content_map.keys())[hit['corpus_id']]
            content = self.file_content_map[file_path]
            score = hit['score']
            results.append((file_path, content, score))
        
        return results


def main():
    """Streamlitアプリのメイン関数"""
    st.title("Obsidianノート検索アプリ")
    
    # インデックスとマッピングファイルのパス
    index_path = os.path.join(os.getcwd(), 'obsidian_notes_index.npy')
    map_path = os.path.join(os.getcwd(), 'file_content_map.json')
    
    # ファイルの存在確認
    if not os.path.exists(index_path) or not os.path.exists(map_path):
        st.error(f"インデックスファイルまたはマッピングファイルが見つかりません。以下のパスを確認してください：\n"
                f"- インデックス: {index_path}\n"
                f"- マッピング: {map_path}")
        st.info("まずインデックスを作成するには、以下のコマンドを実行してください：\n"
               "```\npython -m obsidian_search_app.cli index --directory /Users/io/Documents/Obsidian\n```")
        return
    
    # 検索機能
    searcher = ObsidianSearcher(index_path, map_path)
    
    query = st.text_input("検索クエリを入力してください")
    
    if st.button("検索"):
        if query:
            with st.spinner("検索中..."):
                results = searcher.search(query)
            
            if results:
                st.success(f"{len(results)}件の結果が見つかりました")
                for file_path, content, score in results:
                    # ファイルパスをObsidianのURIスキームで表示
                    obsidian_uri = f"obsidian://open?vault=Obsidian&file={file_path.replace('/Users/io/Documents/Obsidian/', '').replace('.md', '')}"
                    
                    with st.expander(f"{os.path.basename(file_path)} (スコア: {score:.4f})"):
                        st.markdown(f"**ファイル**: [{file_path}]({obsidian_uri})")
                        st.markdown(f"**スコア**: {score:.4f}")
                        st.markdown("**内容の一部**:")
                        st.markdown(content[:500] + "..." if len(content) > 500 else content)
            else:
                st.warning("検索結果が見つかりませんでした")
        else:
            st.warning("検索クエリを入力してください")


if __name__ == "__main__":
    main()
