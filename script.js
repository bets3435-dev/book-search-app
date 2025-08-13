// API 설정과 상태
const API_BASE = 'https://book-search-app-ol4f.onrender.com';
let currentPage = 1;
const pageSize = 20; // 한 페이지에 표시할 항목 수
let lastTotal = 0;

// DOM 요소들
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const categoryFilter = document.getElementById('categoryFilter');
const sortFilter = document.getElementById('sortFilter');
const bookResults = document.getElementById('bookResults'); // tbody를 가리킴
const resultsCount = document.getElementById('resultsCount');
const loadingSpinner = document.getElementById('loadingSpinner');
const noResults = document.getElementById('noResults');
const paginationEl = document.getElementById('pagination');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const pageInfoEl = document.getElementById('pageInfo');

// KDC 분류 매핑 객체
const kdcMap = {
    '0': '총류',
    '1': '철학',
    '2': '종교',
    '3': '사회과학',
    '4': '자연과학',
    '5': '기술과학',
    '6': '예술',
    '7': '언어',
    '8': '문학',
    '9': '역사'
};

// KDC 코드를 분류명으로 변환하는 함수
function getKdcClassName(category) {
    if (!category || typeof category !== 'string') {
        return '기타';
    }
    const firstDigit = category.charAt(0);
    return kdcMap[firstDigit] || '기타';
}


// 검색 실행
async function searchBooks(page = 1) {
    const searchTerm = searchInput.value.trim();
    const selectedCategory = categoryFilter.value; // '0', '1' 등의 숫자가 들어옴
    const selectedSort = sortFilter.value;

    currentPage = page;
    showLoading();

    try {
        const url = new URL(`${API_BASE}/search`);
        if (searchTerm) url.searchParams.set('q', searchTerm);
        // selectedCategory 값이 있을 때만 category 파라미터를 추가
        if (selectedCategory) url.searchParams.set('category', selectedCategory);
        if (selectedSort && selectedSort !== 'relevance') {
            url.searchParams.set('sort', selectedSort);
        }
        url.searchParams.set('page', String(currentPage));
        url.searchParams.set('size', String(pageSize));

        const resp = await fetch(url.toString());
        if (!resp.ok) throw new Error('API 오류');
        const data = await resp.json();

        lastTotal = data.total || 0;
        displayResults(data.items.map(normalizeBook), lastTotal);
        updatePagination();
    } catch (e) {
        console.error("API 호출 실패:", e);
        hideLoading();
        showError("데이터를 불러오는 데 실패했습니다. 잠시 후 다시 시도해 주세요.");
    }
}

// 결과 표시
function displayResults(books, total = 0) {
    hideLoading();
    bookResults.innerHTML = ''; // 이전 결과 비우기

    if (!books || books.length === 0) {
        showNoResults();
        return;
    }

    resultsCount.textContent = `총 ${total}건의 검색 결과`;
    resultsCount.style.display = 'block';

    const tableRows = books.map(createBookTableRow).join('');
    bookResults.innerHTML = tableRows;
}

// 테이블 행(row) HTML 생성 함수
function createBookTableRow(book) {
    const publisher = book.publisher ? book.publisher.replace(/,\s*$/, '').trim() : '-';

    let publishDate = book.publishDate || '정보 없음';
    if (typeof publishDate === 'number') {
        publishDate = String(Math.floor(publishDate));
    } else if (typeof publishDate === 'string' && publishDate.includes('-')) {
        publishDate = publishDate.split('-')[0];
    }

    const kdcClassName = getKdcClassName(book.category);

    return `
        <tr>
            <td>${book.title || '-'}</td>
            <td>${book.author || '-'}</td>
            <td>${publisher}</td>
            <td>${kdcClassName}</td>
            <td>${publishDate}</td>
        </tr>
    `;
}

// 데이터 필드 이름 통일 및 기본값 처리 함수
function normalizeBook(book) {
    return {
        title: book.title,
        author: book.author,
        publisher: book.publisher,
        category: book.category,
        publishDate: book.publishDate || book.publish_date,
    };
}


// --- 나머지 유틸리티 및 이벤트 리스너 함수들 ---

function updatePagination() {
    const totalPages = Math.max(1, Math.ceil(lastTotal / pageSize));
    paginationEl.style.display = lastTotal > 0 ? 'flex' : 'none';
    pageInfoEl.textContent = `${currentPage} / ${totalPages}`;
    prevPageBtn.disabled = currentPage <= 1;
    nextPageBtn.disabled = currentPage >= totalPages;
}

prevPageBtn.addEventListener('click', () => {
    if (currentPage > 1) searchBooks(currentPage - 1);
});

nextPageBtn.addEventListener('click', () => {
    const totalPages = Math.max(1, Math.ceil(lastTotal / pageSize));
    if (currentPage < totalPages) searchBooks(currentPage + 1);
});

function showLoading() {
    loadingSpinner.style.display = 'block';
    bookResults.innerHTML = '';
    resultsCount.style.display = 'none';
    noResults.style.display = 'none';
    paginationEl.style.display = 'none';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function showNoResults() {
    resultsCount.style.display = 'none';
    noResults.style.display = 'block';
}

function showError(message) {
    noResults.querySelector('p').textContent = message;
    noResults.style.display = 'block';
}

// 이벤트 리스너 연결
searchBtn.addEventListener('click', () => searchBooks(1));
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchBooks(1);
});
categoryFilter.addEventListener('change', () => searchBooks(1));
sortFilter.addEventListener('change', () => searchBooks(1));

// 페이지 첫 로드 시, 초기 검색을 실행
document.addEventListener('DOMContentLoaded', () => {
    const tableHeader = document.querySelector('#bookResultsTable thead tr');
    if (tableHeader) {
        tableHeader.innerHTML = `
            <th>제목</th>
            <th>저자</th>
            <th>출판사</th>
            <th>분류</th>
            <th>출판연도</th>
        `;
    }
    searchBooks(1);
});
