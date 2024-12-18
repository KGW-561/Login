function enableEdit(commentId) {
    console.log("Enable edit clicked for comment ID: ", commentId);
    const commentText = document.getElementById(`comment-text-${commentId}`);
    const editForm = document.getElementById(`edit-form-${commentId}`);
    if (!commentText) {
        console.error(`Element with ID comment-text-${commentId} not found`);
        return;
    }
    if (!editForm) {
        console.error(`Element with ID edit-form-${commentId} not found`);
        return;
    }
    // 숨기기: 기존 댓글 텍스트
    commentText.style.display = 'none';
    // 표시하기: 댓글 수정 폼
    editForm.style.display = 'block';
}

function cancelEdit(commentId) {
    // 표시하기: 기존 댓글 텍스트
    document.getElementById(`comment-text-${commentId}`).style.display = 'block';

    // 숨기기: 댓글 수정 폼
    document.getElementById(`edit-form-${commentId}`).style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function () {
    const maxLength = 100;

    // 댓글 입력 제한 함수
    function validateInputLength(inputField, errorField) {
        const inputValue = inputField.value;

        if (inputValue.length > maxLength) {
            errorField.textContent = "글씨를 100자 이내로 입력하세요";
            errorField.style.color = "red";
            return false;
        } else {
            errorField.textContent = ""; // 에러 메시지 제거
            return true;
        }
    }

    // 댓글 입력 처리
    const commentForm = document.querySelector(".comment-form");
    const commentInput = document.querySelector(".comment-input");
    const commentError = document.createElement("div");
    commentError.classList.add("error-message");
    commentForm.insertBefore(commentError, commentForm.lastChild);

    commentForm.addEventListener("submit", function (event) {
        const isValid = validateInputLength(commentInput, commentError);
        if (!isValid) {
            event.preventDefault(); // 폼 제출 중단
        }
    });

    // 댓글 수정 처리
    const editForms = document.querySelectorAll("form[id^='edit-form-']");
    editForms.forEach(function (form) {
        const editInput = form.querySelector(".comment-edit-input");
        const editError = document.createElement("div");
        editError.classList.add("error-message");
        form.insertBefore(editError, form.lastChild);

        form.addEventListener("submit", function (event) {
            const isValid = validateInputLength(editInput, editError);
            if (!isValid) {
                event.preventDefault(); // 폼 제출 중단
            }
        });
    });
});


