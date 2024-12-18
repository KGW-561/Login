document.addEventListener("DOMContentLoaded", () => {

    // 비밀번호 검증 함수
    document.getElementById("password").addEventListener("input", async() => {

        const passwordInput = document.getElementById("password").value; // 비밀번호 입력 값
        const passwordValidation = document.getElementById("password-validation"); // 입력란 밑 경고메세지
        const passwordInputElement = document.getElementById("password");     // password를 받아옴 나중에 제출할때 검증할때 사용

        let isPasswordValid = false; // 비밀번호 검증 상태 변수
        updatePasswordCheckValidation(); // 비밀번호 확인 상태 업데이트


        // 비밀번호 규격 체크 (8자 이상, 64자 이하, 특수문자, 대/소문자, 숫자 포함)
        const passwordPattern = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,64}$/;
        if (!passwordPattern.test(passwordInput)) {
            passwordValidation.textContent = "비밀번호는 8자 이상 64자 이하, 특수문자, 영어, 숫자를 포함하여야 합니다.";
            passwordValidation.style.color = "red";
            isPasswordValid = false;
            passwordInputElement.dataset.isValid = isPasswordValid;
            return;
        }
        // 비밀번호 중복 확인
        isPasswordValid = await checkPasswordDuplicate(passwordInput); // 서버에서 중복 체크 결과 받기

        if(!isPasswordValid) {
            passwordValidation.textContent = "동일한 비밀번호는 사용할 수 없습니다.";
            passwordValidation.style.color = "red";
            isPasswordValid = false;
            passwordInputElement.dataset.isValid = isPasswordValid;
            return;
        } else {
            // 성공 메시지
            passwordValidation.textContent = "사용 가능한 비밀번호입니다.";
            passwordValidation.style.color = "green";
            isPasswordValid = true;
        }
        // 비밀번호 검증 상태 변수 설정( 회원가입 제출시 비밀번호란 검증)
        passwordInputElement.dataset.isValid = isPasswordValid;
    });

    //비밀번호-체크(같은값인지) 함수
    document.getElementById("password-check").addEventListener("input", () => {
        const passwordInput = document.getElementById("password").value;    //비밀번호 입력값
        const passwordCheckInput = document.getElementById("password-check").value; //비밀번호확인 입력값
        const passwordCheckValidation = document.getElementById("password-check-validation");  //입력란 밑 경고메세지
        const passwordCheckInputElement = document.getElementById("password-check");     // password-check를 받아옴 나중에 제출할때 검증할때 사용

        let isPasswordCheckValid = false; // 비밀번호체크 검증 상태 변수
        updatePasswordCheckValidation();
    });

    // 폼 제출 시 이메일 검증 상태 확인
    document.querySelector("form").addEventListener("submit", (event) => {
        const passwordInput = document.getElementById("password").value;
        const passwordValidation = document.getElementById("password-validation"); // 입력란 밑 경고메세지
        const passwordCheckInput = document.getElementById("password-check").value; //비밀번호확인 입력값
        const passwordCheckValidation = document.getElementById("password-check-validation");  //입력란 밑 경고메세지
        const isPasswordValid = document.getElementById("password").dataset.isValid === "true"; // 비밀번호 검증 상태 읽기
        const isPasswordCheckValid = document.getElementById("password-check").dataset.isValid === "true"; // 비밀번호체크 검증 상태 읽기

        // 비밀번호 필수 항목 체크
        if (passwordInput === "") { // 입력값이 없으면 실행
            event.preventDefault(); // 제출 중단
            passwordValidation.textContent = "비밀번호는 필수 항목입니다.";
            passwordValidation.style.color = "red";
            isPasswordValid = false;
            return;
        }

        // 비밀번호 확인 필수 항목 체크
        if (passwordCheckInput === "") { // 입력값이 없으면 실행
            event.preventDefault(); // 제출 중단
            passwordCheckValidation.textContent = "비밀번호확인은 필수 항목입니다.";
            passwordCheckValidation.style.color = "red";
            isPasswordCheckValid = false;
            return;
        }

        if (!isPasswordValid) {
            event.preventDefault(); // 제출 중단
            alert("입력란 경고문을 확인해 주세요!");
            return;
        }
        if (!isPasswordCheckValid) {
            event.preventDefault(); // 제출 중단
            alert("비밀번호가 일치하지 않습니다.");
            return;
        }
    });
});

// 비밀번호 확인 상태를 업데이트하는 함수
function updatePasswordCheckValidation() {
    const passwordInput = document.getElementById("password").value;
    const passwordCheckInput = document.getElementById("password-check").value;
    const passwordCheckValidation = document.getElementById("password-check-validation");
    const passwordCheckInputElement = document.getElementById("password-check"); // 비밀번호체크 검증 상태 읽기

    if (passwordCheckInput === "") {
        return;
    }

    if (passwordInput === passwordCheckInput) {
        passwordCheckValidation.textContent = "비밀번호가 일치합니다.";
        passwordCheckValidation.style.color = "green";
        passwordCheckInputElement.dataset.isValid = true; // 유효 상태로 설정
    } else {
        passwordCheckValidation.textContent = "비밀번호가 일치하지 않습니다.";
        passwordCheckValidation.style.color = "red";
        passwordCheckInputElement.dataset.isValid = false; // 무효 상태로 설정
    }
}

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
        if (data) { // 비밀번호가 일치하면 false
            return false;
        } else { // 비밀번호가 일치하지 않으면 true
            return true;
        }
    } catch (error) {
        // 오류 처리
        console.error('Error:', error);
        return false;
    }
}


