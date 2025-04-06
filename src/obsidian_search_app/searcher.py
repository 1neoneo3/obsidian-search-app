"""
Obsidianノートの検索モジュール
"""

import json
import numpy as np
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
