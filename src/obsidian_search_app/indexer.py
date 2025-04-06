"""
Obsidianノートのインデックス作成モジュール
"""

import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer


def read_markdown_files(directory):
    """指定されたディレクトリ内のMarkdownファイルを読み込む"""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    markdown_files.append((file_path, content))
    return markdown_files


def create_embeddings(texts, model):
    """テキストのリストから埋め込みベクトルを作成する"""
    embeddings = model.encode(texts)
    return embeddings


def index_notes(directory, output_dir=None):
    """Obsidianノートをインデックス化する"""
    if output_dir is None:
        output_dir = os.getcwd()
    
    # モデルの読み込み
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # ファイル読み込み
    markdown_files = read_markdown_files(directory)
    
    # ファイル内容をインデックス化
    texts = [content for _, content in markdown_files]
    embeddings = create_embeddings(texts, model)
    
    # インデックスを保存
    index_path = os.path.join(output_dir, 'obsidian_notes_index.npy')
    np.save(index_path, embeddings)
    
    # ファイルパスと内容の対応を保存
    file_content_map = {file_path: content for file_path, content in markdown_files}
    map_path = os.path.join(output_dir, 'file_content_map.json')
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(file_content_map, f, ensure_ascii=False, indent=4)
    
    return index_path, map_path
