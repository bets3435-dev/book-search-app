# 도서 검색 시스템 📚

도서 목록을 검색할 수 있는 모던한 웹 페이지입니다.

## ✨ 주요 기능

- **실시간 검색**: 도서 제목, 저자, 출판사, 설명으로 검색
- **카테고리 필터링**: 소설, 자기계발, 경제경영, 역사, 과학, 예술, 여행, 요리 카테고리별 필터링
- **정렬 기능**: 관련도순, 제목순, 저자순, 출판일순으로 정렬
- **반응형 디자인**: 모바일과 데스크톱에서 모두 최적화된 UI
- **도서 상세 정보**: 도서 카드 클릭 시 상세 정보 모달 표시

## 🚀 시작하기

1. 프로젝트 폴더로 이동:
   ```bash
   cd book-search-app
   ```

2. `index.html` 파일을 웹 브라우저에서 열기

3. 검색창에 원하는 키워드를 입력하고 검색 버튼 클릭

## 🛠️ 기술 스택

- **HTML5**: 시맨틱 마크업
- **CSS3**: 모던한 스타일링과 애니메이션
- **JavaScript (ES6+)**: 검색 및 필터링 로직
- **Font Awesome**: 아이콘
- **Google Fonts**: Noto Sans KR 폰트

## 📁 파일 구조

```
book-search-app/
├── index.html          # 메인 HTML 파일
├── styles.css          # CSS 스타일시트
├── script.js           # JavaScript 기능
└── README.md           # 프로젝트 설명서
```

## 🔍 사용법

### 기본 검색
- 검색창에 도서 제목, 저자, 출판사 등을 입력
- Enter 키 또는 검색 버튼 클릭

### 필터링
- **카테고리**: 특정 카테고리의 도서만 표시
- **정렬**: 검색 결과를 원하는 기준으로 정렬

### 도서 상세 정보
- 도서 카드를 클릭하면 상세 정보 모달이 표시됩니다
- 모달 외부를 클릭하거나 X 버튼으로 닫을 수 있습니다

## 🎨 디자인 특징

- **그라데이션 배경**: 시각적으로 매력적인 UI
- **카드 기반 레이아웃**: 깔끔하고 직관적인 도서 표시
- **호버 효과**: 사용자 상호작용을 위한 부드러운 애니메이션
- **모바일 최적화**: 모든 화면 크기에서 최적의 경험 제공

## 📱 반응형 지원

- 데스크톱: 3열 그리드 레이아웃
- 태블릿: 2열 그리드 레이아웃
- 모바일: 1열 레이아웃으로 최적화

## 🔮 향후 개선 계획

- [ ] 실제 도서 API 연동
- [ ] 사용자 계정 및 찜하기 기능
- [ ] 도서 리뷰 및 평점 시스템
- [ ] 고급 검색 필터 (가격, 페이지 수 등)
- [ ] 다크 모드 지원

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

**만든이**: AI Assistant  
**제작일**: 2024년 

## 🗃️ 대용량 CSV 연동 (백엔드 API)

수십만 건 데이터는 브라우저에서 직접 처리하기 어렵습니다. FastAPI + SQLite로 검색 API를 제공하고, 프런트엔드는 API를 호출합니다.

### 1) 가상환경 및 패키지 설치
```bash
cd book-search-app
python -m venv venv
venv\Scripts\activate
pip install -r api\requirements.txt
```

### 2) CSV → SQLite 적재
```bash
# 기본 헤더명 가정: title, author, publisher, category, publish_date, description
python api\ingest_csv.py --csv "C:\\path\\to\\your_books.csv"

# 헤더명이 다르면 컬럼 매핑 지정 예시
python api\ingest_csv.py --csv "C:\\data\\books.csv" --title Title --author Author \
  --publisher Publisher --category Category --publish_date Published --description Description
```

### 3) API 서버 실행
```bash
uvicorn api.app_simple:app --host 0.0.0.0 --port 8000
```
- 헬스체크: http://localhost:8000/health
- 검색 API: http://localhost:8000/search?q=검색어&category=소설&sort=title&page=1&size=20

### 4) 프런트엔드 연동
- `script.js` 의 `API_BASE` 는 기본값 `http://localhost:8000` 입니다.
- GitHub Pages에서 접속 시에도 로컬/배포된 API로 호출됩니다(CORS 허용).

### 5) 배포 옵션
- 간단: Render / Railway / Fly.io 등에 FastAPI 배포 후 `API_BASE` 를 해당 URL로 변경
- 고성능: Typesense/MeiliSearch 등의 검색엔진 사용 → API에서 프록시

## 🛒 YES24 도서 정보 연동

### 주요 기능
- **실시간 도서 정보**: YES24에서 최신 가격, 표지 이미지, 재고 정보
- **하이브리드 검색**: 로컬 DB + YES24 정보 병합
- **표지 이미지**: 고화질 도서 표지 이미지 표시
- **가격 정보**: 실시간 가격 및 할인 정보
- **ISBN 연동**: ISBN으로 정확한 도서 정보 매칭

### API 엔드포인트
- `GET /search`: 통합 검색 (로컬 DB + YES24)
- `GET /yes24/search`: YES24 전용 검색
- `GET /yes24/book/{isbn}`: ISBN으로 도서 상세 정보
- `GET /yes24/bestsellers`: 베스트셀러 목록

### 사용법
1. **통합 검색**: 일반 검색 시 자동으로 YES24 정보 연동
2. **YES24 전용**: `use_yes24=true` 파라미터로 YES24만 검색
3. **표지 이미지**: 검색 결과에 자동으로 표지 이미지 표시
4. **가격 정보**: 실시간 가격 및 구매 링크 제공

### 기술적 특징
- **웹 스크래핑**: 공식 API 없이 YES24 웹사이트에서 정보 추출
- **에러 처리**: YES24 서버 장애 시 로컬 DB로 폴백
- **캐싱**: 중복 요청 방지 및 성능 최적화
- **유사도 매칭**: 제목과 저자 기반으로 도서 정보 매칭

--- 