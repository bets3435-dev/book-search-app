import os
import json
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
import pandas as pd

class SemanticSearchEngine:
    def __init__(self, db_path: str = "chroma_db"):
        self.db_path = db_path
        self.model_name = "jhgan/ko-sroberta-multitask"  # 한국어 최적화 모델
        self.embedding_model = SentenceTransformer(self.model_name)
        
        # ChromaDB 클라이언트 초기화
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 컬렉션 생성 또는 가져오기
        self.collection = self.client.get_or_create_collection(
            name="books",
            metadata={"hnsw:space": "cosine"}
        )
    
    def create_context(self, book: Dict) -> str:
        """도서 정보를 검색에 적합한 맥락 텍스트로 변환"""
        context_parts = []
        
        if book.get('title'):
            context_parts.append(f"제목: {book['title']}")
        
        if book.get('author'):
            context_parts.append(f"저자: {book['author']}")
            
        if book.get('publisher'):
            context_parts.append(f"출판사: {book['publisher']}")
            
        if book.get('category'):
            context_parts.append(f"분류: {book['category']}")
            
        if book.get('description'):
            context_parts.append(f"내용: {book['description']}")
            
        if book.get('publish_date'):
            context_parts.append(f"출판일: {book['publish_date']}")
        
        return " | ".join(context_parts)
    
    def add_books(self, books: List[Dict]) -> None:
        """도서 목록을 벡터 DB에 추가"""
        if not books:
            return
            
        contexts = []
        metadatas = []
        ids = []
        
        for book in books:
            context = self.create_context(book)
            contexts.append(context)
            metadatas.append(book)
            ids.append(str(book.get('id', len(ids))))
        
        # 임베딩 생성 및 저장
        embeddings = self.embedding_model.encode(contexts).tolist()
        
        self.collection.add(
            embeddings=embeddings,
            documents=contexts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(books)} books to vector database")
    
    def semantic_search(
        self, 
        query: str, 
        n_results: int = 20,
        use_llm_enhancement: bool = False
    ) -> List[Dict]:
        """시맨틱 검색 수행"""
        if not query.strip():
            return []
        
        # 기본 검색: 사용자 질의를 직접 임베딩
        query_embedding = self.embedding_model.encode([query])
        
        # 벡터 DB에서 유사도 검색
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            include=['metadatas', 'distances']
        )
        
        # 결과 정리
        books = []
        for i, metadata in enumerate(results['metadatas'][0]):
            book = metadata.copy()
            book['similarity_score'] = 1 - results['distances'][0][i]  # 거리를 유사도로 변환
            books.append(book)
        
        # 유사도 순으로 정렬
        books.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return books
    
    def get_recommendation_reason(self, book: Dict, query: str) -> str:
        """도서 추천 이유 생성 (간단한 규칙 기반)"""
        reasons = []
        
        if query.lower() in book.get('title', '').lower():
            reasons.append("검색어가 제목에 포함되어 있습니다")
            
        if query.lower() in book.get('author', '').lower():
            reasons.append("검색어가 저자명과 일치합니다")
            
        if query.lower() in book.get('category', '').lower():
            reasons.append("검색어가 해당 카테고리에 속합니다")
            
        if query.lower() in book.get('description', '').lower():
            reasons.append("검색어가 도서 설명에 포함되어 있습니다")
        
        if not reasons:
            # 유사도 기반 추천 이유
            reasons.append("검색어와 의미적으로 유사한 도서입니다")
        
        return " | ".join(reasons)
    
    def clear_database(self) -> None:
        """벡터 DB 초기화"""
        self.client.delete_collection("books")
        self.collection = self.client.create_collection(
            name="books",
            metadata={"hnsw:space": "cosine"}
        )
        print("Vector database cleared")

# 전역 인스턴스
search_engine = None

def get_search_engine() -> SemanticSearchEngine:
    """검색 엔진 인스턴스 반환 (싱글톤)"""
    global search_engine
    if search_engine is None:
        search_engine = SemanticSearchEngine()
    return search_engine 