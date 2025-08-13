import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Dict, List, Optional
from urllib.parse import quote_plus, urljoin
import json

class Yes24BookAPI:
    def __init__(self):
        self.base_url = "https://www.yes24.com"
        self.search_url = "https://www.yes24.com/24/Goods/Search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def search_books(self, query: str, page: int = 1, max_results: int = 20) -> Dict:
        """도서 검색"""
        try:
            # 검색 URL 구성
            params = {
                'Query': query,
                'QueryType': 'GOODS',
                'SearchTarget': 'BOOK',
                'Page': page,
                'Sort': 'ACCURACY'  # 정확도순
            }
            
            response = requests.get(
                self.search_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            books = self._parse_search_results(soup, max_results)
            
            return {
                'success': True,
                'query': query,
                'total': len(books),
                'page': page,
                'items': books
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'items': []
            }
    
    def _parse_search_results(self, soup: BeautifulSoup, max_results: int) -> List[Dict]:
        """검색 결과 파싱"""
        books = []
        
        # 도서 목록 찾기
        book_items = soup.find_all('div', class_='item_info')
        
        for item in book_items[:max_results]:
            try:
                book = self._extract_book_info(item)
                if book:
                    books.append(book)
            except Exception as e:
                print(f"도서 정보 추출 오류: {e}")
                continue
        
        return books
    
    def _extract_book_info(self, item) -> Optional[Dict]:
        """개별 도서 정보 추출"""
        try:
            # 제목
            title_elem = item.find('a', class_='gd_name')
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # 링크
            link = title_elem.get('href') if title_elem else ''
            if link and not link.startswith('http'):
                link = urljoin(self.base_url, link)
            
            # 저자
            author_elem = item.find('span', class_='authPub')
            author = author_elem.get_text(strip=True) if author_elem else ''
            
            # 출판사
            publisher_elem = item.find('span', class_='pub')
            publisher = publisher_elem.get_text(strip=True) if publisher_elem else ''
            
            # 가격
            price_elem = item.find('span', class_='price')
            price = price_elem.get_text(strip=True) if price_elem else ''
            
            # 표지 이미지
            cover_elem = item.find_previous('div', class_='item_img').find('img')
            cover_image = ''
            if cover_elem:
                cover_image = cover_elem.get('src') or cover_elem.get('data-original', '')
                if cover_image and not cover_image.startswith('http'):
                    cover_image = urljoin(self.base_url, cover_image)
            
            # ISBN (링크에서 추출)
            isbn = ''
            if link:
                isbn_match = re.search(r'/(\d+)$', link)
                if isbn_match:
                    isbn = isbn_match.group(1)
            
            return {
                'title': title,
                'author': author,
                'publisher': publisher,
                'price': price,
                'cover_image': cover_image,
                'link': link,
                'isbn': isbn,
                'source': 'yes24'
            }
            
        except Exception as e:
            print(f"도서 정보 추출 중 오류: {e}")
            return None
    
    def get_book_detail(self, book_url: str) -> Dict:
        """도서 상세 정보 조회"""
        try:
            response = requests.get(book_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상세 정보 추출
            detail = self._parse_book_detail(soup)
            
            return {
                'success': True,
                'detail': detail
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_book_detail(self, soup: BeautifulSoup) -> Dict:
        """도서 상세 정보 파싱"""
        detail = {}
        
        try:
            # 상세 설명
            desc_elem = soup.find('div', class_='gd_detail')
            if desc_elem:
                detail['description'] = desc_elem.get_text(strip=True)
            
            # 목차
            toc_elem = soup.find('div', class_='gd_toc')
            if toc_elem:
                detail['table_of_contents'] = toc_elem.get_text(strip=True)
            
            # 출간일
            pub_date_elem = soup.find('span', class_='gd_date')
            if pub_date_elem:
                detail['publication_date'] = pub_date_elem.get_text(strip=True)
            
            # 페이지 수
            pages_elem = soup.find('span', class_='gd_pages')
            if pages_elem:
                detail['pages'] = pages_elem.get_text(strip=True)
            
            # 크기
            size_elem = soup.find('span', class_='gd_size')
            if size_elem:
                detail['size'] = size_elem.get_text(strip=True)
            
        except Exception as e:
            print(f"상세 정보 파싱 오류: {e}")
        
        return detail
    
    def search_by_isbn(self, isbn: str) -> Dict:
        """ISBN으로 도서 검색"""
        return self.search_books(isbn, page=1, max_results=5)
    
    def get_bestsellers(self, category: str = 'BOOK', page: int = 1) -> Dict:
        """베스트셀러 조회"""
        try:
            url = f"{self.base_url}/24/Category/BestSeller"
            params = {
                'CategoryNumber': '001',
                'Page': page
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            books = self._parse_search_results(soup, 20)
            
            return {
                'success': True,
                'category': category,
                'page': page,
                'items': books
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'items': []
            }

# 사용 예시
if __name__ == "__main__":
    api = Yes24BookAPI()
    
    # 검색 테스트
    result = api.search_books("파이썬 프로그래밍", page=1, max_results=5)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 