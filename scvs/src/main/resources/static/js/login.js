document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // 폼 기본 제출 동작 방지
        const emailInput = document.getElementById('email').value;  // 이메일 입력값
        const passwordInput = document.getElementById('password').value; // 비밀번호 입력값
        const loginValidation = document.getElementById("login-validation"); // 입력란 밑 경고메세지

        // 이메일 필수 항목 체크
        if (emailInput === "") { // 입력값이 없으면 실행
            loginValidation.textContent = "이메일을 입력하세요.";
            loginValidation.style.color = "red";
            return;
        } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(emailInput)) { // 이메일형식 @ . 을 검사
            loginValidation.textContent = "이메일 형식이 아닙니다.";
            loginValidation.style.color = "red";
            return;
        }

        // 비밀번호 공백체크
        if (passwordInput === ""){
           loginValidation.textContent = "비밀번호를 입력하세요.";
           loginValidation.style.color = "red";
           return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    email: emailInput,
                    password: passwordInput
                })
            });

            if (!response.ok) {
                // 실패 시 처리
                loginValidation.textContent = "이메일또는 비밀번호가 일치하지 않습니다.";
                loginValidation.style.color = "red";
                return;
            }
            // 성공 시 처리
            window.location.href = '/'; // 성공 후 리디렉션
        } catch (error) {
        }
    });
});
