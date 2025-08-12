// 샘플 도서 데이터
const sampleBooks = [
    {
        id: 1,
        title: "1984",
        author: "조지 오웰",
        publisher: "민음사",
        category: "소설",
        publishDate: "2020-01-15",
        description: "디스토피아 소설의 대표작으로, 전체주의 사회의 모습을 그린 작품입니다."
    },
    {
        id: 2,
        title: "자기계발의 정석",
        author: "김성민",
        publisher: "비즈니스북스",
        category: "자기계발",
        publishDate: "2023-03-20",
        description: "성공적인 삶을 위한 자기계발 방법론을 다룬 실용적인 가이드입니다."
    },
    {
        id: 3,
        title: "경제학 입문",
        author: "박경철",
        publisher: "한국경제신문사",
        category: "경제경영",
        publishDate: "2022-11-10",
        description: "경제학의 기본 개념과 원리를 쉽게 설명한 입문서입니다."
    },
    {
        id: 4,
        title: "한국사 100장면",
        author: "이영훈",
        publisher: "책과함께",
        category: "역사",
        publishDate: "2021-06-25",
        description: "한국 역사의 중요한 순간들을 100개의 장면으로 재구성한 책입니다."
    },
    {
        id: 5,
        title: "우주의 신비",
        author: "최재천",
        publisher: "사이언스북스",
        category: "과학",
        publishDate: "2023-08-15",
        description: "우주의 탄생부터 현재까지의 과정을 흥미롭게 설명한 과학 도서입니다."
    },
    {
        id: 6,
        title: "현대미술의 이해",
        author: "김미영",
        publisher: "예술의전당",
        category: "예술",
        publishDate: "2022-04-12",
        description: "20세기 현대미술의 흐름과 주요 작가들을 소개하는 예술 도서입니다."
    },
    {
        id: 7,
        title: "일본 여행 가이드",
        author: "이준호",
        publisher: "여행출판사",
        category: "여행",
        publishDate: "2023-05-30",
        description: "일본의 주요 관광지와 맛집, 숙박 정보를 담은 실용적인 여행 가이드입니다."
    },
    {
        id: 8,
        title: "한식의 맛과 멋",
        author: "정순자",
        publisher: "요리문화사",
        category: "요리",
        publishDate: "2022-09-18",
        description: "전통 한식의 조리법과 문화적 의미를 다룬 요리 도서입니다."
    },
    {
        id: 9,
        title: "디지털 마케팅 전략",
        author: "최지원",
        publisher: "마케팅북스",
        category: "경제경영",
        publishDate: "2023-07-22",
        description: "디지털 시대의 마케팅 전략과 실무 방법을 다룬 전문서입니다."
    },
    {
        id: 10,
        title: "심리학의 발견",
        author: "김민수",
        publisher: "심리학사",
        category: "과학",
        publishDate: "2021-12-05",
        description: "인간의 마음과 행동을 이해하는 심리학의 핵심 개념을 소개합니다."
    }
];

// DOM 요소들
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const categoryFilter = document.getElementById('categoryFilter');
const sortFilter = document.getElementById('sortFilter');
const bookResults = document.getElementById('bookResults');
const resultsCount = document.getElementById('resultsCount');
const loadingSpinner = document.getElementById('loadingSpinner');
const noResults = document.getElementById('noResults');

// 검색 기능
function searchBooks() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    const selectedCategory = categoryFilter.value;
    const selectedSort = sortFilter.value;
    
    // 로딩 표시
    showLoading();
    
    // 검색 지연 시뮬레이션 (실제 API 호출 시에는 제거)
    setTimeout(() => {
        let filteredBooks = sampleBooks.filter(book => {
            const matchesSearch = !searchTerm || 
                book.title.toLowerCase().includes(searchTerm) ||
                book.author.toLowerCase().includes(searchTerm) ||
                book.publisher.toLowerCase().includes(searchTerm) ||
                book.description.toLowerCase().includes(searchTerm);
            
            const matchesCategory = !selectedCategory || book.category === selectedCategory;
            
            return matchesSearch && matchesCategory;
        });
        
        // 정렬
        filteredBooks = sortBooks(filteredBooks, selectedSort);
        
        // 결과 표시
        displayResults(filteredBooks);
    }, 500);
}

// 도서 정렬
function sortBooks(books, sortType) {
    switch(sortType) {
        case 'title':
            return books.sort((a, b) => a.title.localeCompare(b.title, 'ko'));
        case 'author':
            return books.sort((a, b) => a.author.localeCompare(b.author, 'ko'));
        case 'date':
            return books.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate));
        default: // relevance
            return books;
    }
}

// 검색 결과 표시
function displayResults(books) {
    hideLoading();
    
    if (books.length === 0) {
        showNoResults();
        return;
    }
    
    // 결과 개수 표시
    resultsCount.textContent = `검색 결과: ${books.length}건`;
    resultsCount.style.display = 'block';
    
    // 도서 카드 생성
    const bookCards = books.map(book => createBookCard(book)).join('');
    bookResults.innerHTML = bookCards;
    bookResults.style.display = 'grid';
    
    // 도서 카드 클릭 이벤트
    addBookCardEvents();
}

// 도서 카드 생성
function createBookCard(book) {
    const firstLetter = book.title.charAt(0);
    return `
        <div class="book-card" data-book-id="${book.id}">
            <div class="book-cover">
                <i class="fas fa-book"></i>
            </div>
            <div class="book-info">
                <h3>${book.title}</h3>
                <div class="author">저자: ${book.author}</div>
                <div class="publisher">출판사: ${book.publisher}</div>
                <div class="category">${book.category}</div>
            </div>
        </div>
    `;
}

// 도서 카드 클릭 이벤트
function addBookCardEvents() {
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
        card.addEventListener('click', () => {
            const bookId = card.getAttribute('data-book-id');
            const book = sampleBooks.find(b => b.id == bookId);
            if (book) {
                showBookDetail(book);
            }
        });
    });
}

// 도서 상세 정보 표시
function showBookDetail(book) {
    const detailHTML = `
        <div class="book-detail-overlay">
            <div class="book-detail-modal">
                <div class="modal-header">
                    <h2>${book.title}</h2>
                    <button class="close-btn" onclick="closeBookDetail()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-content">
                    <div class="book-cover-large">
                        <i class="fas fa-book"></i>
                    </div>
                    <div class="book-detail-info">
                        <p><strong>저자:</strong> ${book.author}</p>
                        <p><strong>출판사:</strong> ${book.publisher}</p>
                        <p><strong>카테고리:</strong> ${book.category}</p>
                        <p><strong>출판일:</strong> ${formatDate(book.publishDate)}</p>
                        <p><strong>설명:</strong> ${book.description}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 기존 모달 제거
    const existingModal = document.querySelector('.book-detail-overlay');
    if (existingModal) {
        existingModal.remove();
    }
    
    // 새 모달 추가
    document.body.insertAdjacentHTML('beforeend', detailHTML);
    
    // 모달 외부 클릭 시 닫기
    const overlay = document.querySelector('.book-detail-overlay');
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeBookDetail();
        }
    });
}

// 도서 상세 정보 닫기
function closeBookDetail() {
    const modal = document.querySelector('.book-detail-overlay');
    if (modal) {
        modal.remove();
    }
}

// 날짜 포맷팅
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR');
}

// 로딩 표시
function showLoading() {
    loadingSpinner.style.display = 'block';
    bookResults.style.display = 'none';
    resultsCount.style.display = 'none';
    noResults.style.display = 'none';
}

// 로딩 숨기기
function hideLoading() {
    loadingSpinner.style.display = 'none';
}

// 검색 결과 없음 표시
function showNoResults() {
    resultsCount.style.display = 'none';
    bookResults.style.display = 'none';
    noResults.style.display = 'block';
}

// 이벤트 리스너 등록
searchBtn.addEventListener('click', searchBooks);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchBooks();
    }
});

categoryFilter.addEventListener('change', searchBooks);
sortFilter.addEventListener('change', searchBooks);

// 페이지 로드 시 초기 검색 결과 표시
document.addEventListener('DOMContentLoaded', () => {
    searchBooks();
});

// 모달 스타일 추가
const modalStyles = `
    <style>
        .book-detail-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .book-detail-modal {
            background: white;
            border-radius: 20px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 25px;
            border-bottom: 1px solid #e1e5e9;
        }
        
        .modal-header h2 {
            margin: 0;
            color: #333;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #666;
            padding: 5px;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        
        .close-btn:hover {
            background: #f0f0f0;
            color: #333;
        }
        
        .modal-content {
            padding: 25px;
        }
        
        .book-cover-large {
            width: 100%;
            height: 250px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4rem;
        }
        
        .book-detail-info p {
            margin-bottom: 12px;
            line-height: 1.6;
        }
        
        .book-detail-info strong {
            color: #333;
            margin-right: 8px;
        }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', modalStyles); 