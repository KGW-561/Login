document.addEventListener("DOMContentLoaded", function () {
    // 검색 및 필터링 관련 요소
    const watchlistSearchInput = document.getElementById("watchlistSearchInput");
    const watchlistTable = document.getElementById("watchlistTable");
    const cancelSearchBtn = document.getElementById("cancelSearchBtn");

    const allTickersSearchInput = document.getElementById("allTickersSearchInput");
    const allTickersTable = document.getElementById("allTickersTable");
    const cancelALLTickersSearchBtn = document.getElementById("cancelALLTickersSearchBtn");

    const watchlistSearchForm = document.getElementById("watchlistSearchForm");
    const allTickerSearchForm = document.getElementById("allTickerSearchForm");

    // 폼 제출 방지 (Enter 키 사용 시 새로고침 방지)
    watchlistSearchForm.addEventListener("submit", function (event) {
        event.preventDefault();
    });

    allTickerSearchForm.addEventListener("submit", function (event) {
        event.preventDefault();
    });

    // 관심 목록 검색 필터링
    watchlistSearchInput.addEventListener("input", function () {
        filterTable(watchlistTable, watchlistSearchInput.value);
    });

    cancelSearchBtn.addEventListener("click", function () {
        watchlistSearchInput.value = ""; // 검색 필드 초기화
        filterTable(watchlistTable, ""); // 필터 초기화
    });

    // 전체 티커 검색 필터링
    allTickersSearchInput.addEventListener("input", function () {
        filterTable(allTickersTable, allTickersSearchInput.value);
    });

    cancelALLTickersSearchBtn.addEventListener("click", function () {
        allTickersSearchInput.value = ""; // 검색 필드 초기화
        filterTable(allTickersTable, ""); // 필터 초기화
    });

    // 테이블 필터링 함수
    function filterTable(table, filterText) {
        const rows = table.querySelectorAll("tbody tr");
        const filter = filterText.toLowerCase();

        rows.forEach((row) => {
            const companyCell = row.querySelector("td:nth-child(1)"); // 첫 번째 셀
            const codeCell = row.querySelector("td:nth-child(2)"); // 두 번째 셀

            if (companyCell && codeCell) {
                const companyName = companyCell.textContent.toLowerCase();
                const code = codeCell.textContent.toLowerCase();

                // 검색어와 일치하는 행만 보이도록 설정
                if (companyName.includes(filter) || code.includes(filter)) {
                    row.style.display = ""; // 보이기
                } else {
                    row.style.display = "none"; // 숨기기
                }
            }
        });
    }

    // 페이지네이션 관련 설정
    const rowsPerPage = 7;

    // 관심 목록 초기화
    const watchlistRows = document.querySelectorAll("#watchlistTable tbody tr");
    const watchlistLoadMoreBtn = document.getElementById("loadMoreBtn");
    let watchlistCurrentIndex = 0;

    // 전체 티커 목록 초기화
    const allTickersRows = document.querySelectorAll("#allTickersTable tbody tr");
    const allTickersLoadMoreBtn = document.getElementById("allTickersLoadMoreBtn");
    let allTickersCurrentIndex = 0;

    // 공통 행 표시 함수
    function showRows(rows, currentIndex, rowsPerPage, loadMoreBtn) {
        for (let i = currentIndex; i < currentIndex + rowsPerPage && i < rows.length; i++) {
            rows[i].style.display = ""; // 보이기
        }
        currentIndex += rowsPerPage;

        if (currentIndex >= rows.length) {
            loadMoreBtn.style.display = "none"; // 더보기 버튼 숨기기
        } else {
            loadMoreBtn.style.display = "block"; // 더보기 버튼 보이기
        }

        return currentIndex; // 업데이트된 인덱스 반환
    }

    // 초기화: 모든 행 숨기기
    watchlistRows.forEach((row) => (row.style.display = "none"));
    allTickersRows.forEach((row) => (row.style.display = "none"));

    // 초기 행 표시
    watchlistCurrentIndex = showRows(watchlistRows, watchlistCurrentIndex, rowsPerPage, watchlistLoadMoreBtn);
    allTickersCurrentIndex = showRows(allTickersRows, allTickersCurrentIndex, rowsPerPage, allTickersLoadMoreBtn);

    // 관심 목록 더보기 버튼
    watchlistLoadMoreBtn.addEventListener("click", function () {
        watchlistCurrentIndex = showRows(watchlistRows, watchlistCurrentIndex, rowsPerPage, watchlistLoadMoreBtn);
    });

    // 전체 티커 더보기 버튼
    allTickersLoadMoreBtn.addEventListener("click", function () {
        allTickersCurrentIndex = showRows(allTickersRows, allTickersCurrentIndex, rowsPerPage, allTickersLoadMoreBtn);
    });
});
