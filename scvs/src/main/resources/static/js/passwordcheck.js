document.addEventListener("DOMContentLoaded", () => {

    // 폼 제출 시 비밀번호 검증 상태 확인
    document.querySelector("form").addEventListener("submit", async (event) => {
        event.preventDefault(); // 제출방지
        const passwordInput = document.getElementById("password").value; // 비밀번호 입력 값
        let isPasswordValid = false; // 비밀번호 검증 상태 변수

        try {

            // 비밀번호 규격 체크 (8자 이상, 64자 이하, 특수문자, 대/소문자, 숫자 포함)
            const passwordPattern = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,64}$/;
            if (!passwordPattern.test(passwordInput)) {
                alert("비밀번호가 틀립니다.");
                isPasswordValid = false;
                return;
            }
            // 비밀번호 중복 확인
            isPasswordValid = await checkPasswordDuplicate(passwordInput); // 서버에서 중복 체크 결과 받기

            // 비밀번호 중복 여부에 따라 폼 제출 여부 결정
            if (!isPasswordValid) {
                alert("비밀번호가 틀립니다.");
            } else {
                // 성공 시 처리
                window.location.href = '/user/passwordchange'; // 성공 후 리디렉션
            }
        } catch (error) {
            console.error("비밀번호 중복 체크 중 오류 발생:", error);
            alert("비밀번호 중복 체크 중 오류가 발생했습니다.");
        }
    });
});

// 비밀번호 중복 체크 함수
async function checkPasswordDuplicate(passwordInput) {
    try {
        // 비동기 요청을 보낼 API 경로
        const response = await fetch('/api/check-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // 요청 본문이 JSON 형식임을 명시
            },
            body: JSON.stringify({ password: passwordInput })  // 패스워드를 JSON 형태로 전송
        });

        const data = await response.json();  // 응답을 JSON 형태로 파싱

        // 서버에서 받은 응답을 처리
        if (data) { // 비밀번호가 일치하면 true
            return true;
        } else { // 비밀번호가 일치하지 않으면 false
            return false;
        }
    } catch (error) {
        // 오류 처리
        console.error('Error:', error);
        return false;
    }
}
