document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("nickname").dataset.isValid = true;


    // 이메일 입력 시 검증 초기화 (중복확인하고 수정시 제출방지)
    document.getElementById("email").addEventListener("input", () => {
        const emailValidation = document.getElementById("email-validation");
        emailValidation.textContent = "";  // 경고 메시지 초기화
        document.getElementById("email").dataset.isValid = false; // 이메일 검증 상태 초기화
    });

    // 닉네임 입력 시 검증 초기화 (중복확인하고 수정시 제출방지)
    document.getElementById("nickname").addEventListener("input", () => {
        const nicknameValidation = document.getElementById("nickname-validation");
        nicknameValidation.textContent = "";  // 경고 메시지 초기화
        document.getElementById("nickname").dataset.isValid = false; // 닉네임 검증 상태 초기화
    });

    // 이메일 중복 확인 버튼 이벤트 리스너
    document.getElementById("check-email-duplicate").addEventListener("click", async () => {
        const emailInput = document.getElementById("email").value; // 이메일 입력 값
        const emailValidation = document.getElementById("email-validation"); // 입력란 밑 경고메세지
        const emailInputElement = document.getElementById("email");     // email을 받아옴 나중에 제출할때 검증할때 사용
        let isEmailValid = false; // 이메일 검증 상태 변수
        // 이메일 필수 항목 체크
        if (emailInput === "") { // 입력값이 없으면 실행
            emailValidation.textContent = "이메일은 필수 항목입니다.";
            emailValidation.style.color = "red";
            isEmailValid = false;
            return;
        } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(emailInput)) { // 이메일형식 @ . 을 검사
            emailValidation.textContent = "이메일 형식이 아닙니다.";
            emailValidation.style.color = "red";
            isEmailValid = false;
            return;
        } else {
            isEmailValid = await checkEmailDuplicate(emailInput); // 중복체크 함수 > 서버 호출 || 중복이면 isEmailValid = false
        }
        // 이메일 상태 변수 설정( 회원가입 제출시 이메일란 검증)
        emailInputElement.dataset.isValid = isEmailValid;
    });



    // 비밀번호 검증 함수
    document.getElementById("password").addEventListener("input", () => {
        const passwordInput = document.getElementById("password").value; // 비밀번호 입력 값
        const passwordValidation = document.getElementById("password-validation"); // 입력란 밑 경고메세지
        const passwordInputElement = document.getElementById("password");     // password를 받아옴 나중에 제출할때 검증할때 사용

        let isPasswordValid = false; // 비밀번호 검증 상태 변수
        updatePasswordCheckValidation();

        // 비밀번호 필수 항목 체크
        if (passwordInput.trim() === "") { // 입력값이 없으면 실행
            passwordValidation.textContent = "비밀번호는 필수 항목입니다.";
            passwordValidation.style.color = "red";
            isPasswordValid = false;
        }

        // 비밀번호 규격 체크 (8자 이상, 64자 이하, 특수문자, 대/소문자, 숫자 포함)
        const passwordPattern = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,64}$/;
        if (!passwordPattern.test(passwordInput)) {
            passwordValidation.textContent = "비밀번호는 8자 이상 64자 이하, 특수문자, 영어, 숫자를 포함하여야 합니다.";
            passwordValidation.style.color = "red";
            isPasswordValid = false;
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
        const passwordCheckValidation = document.getElementById("Password-check-validation");  //입력란 밑 경고메세지
        const passwordCheckInputElement = document.getElementById("password-check");     // password-check를 받아옴 나중에 제출할때 검증할때 사용

        passwordCheckInputElement.dataset.isValid = false; // 비밀번호체크 검증 상태 변수
        updatePasswordCheckValidation();
    });




 // 닉네임 중복 확인 버튼 이벤트 리스너
  document.getElementById("check-nickname-duplicate").addEventListener("click", async () => {
      const nicknameInput = document.getElementById("nickname").value; // 닉네임 입력값
      const nicknameValidation = document.getElementById("nickname-validation"); //입력란 밑 경고메세지
      const nicknameInputElement = document.getElementById("nickname");     // nickname을 받아옴 나중에 제출할때 검증할때 사용
      let isNicknameValid = false; // 이메일 검증 상태 변수

      // 닉네임이 비어있으면
      if (nicknameInput === "") {
          nicknameValidation.textContent = "닉네임은 필수항목입니다.";
          nicknameValidation.style.color = "red";
          isNicknameValid = false;
          return;
      }

      // 닉네임 유효성 체크 (2~15자, 영/한/숫자, 띄어쓰기 금지)
      const nicknamePattern = /^[a-zA-Z0-9가-힣]{2,15}$/;
      if (!nicknamePattern.test(nicknameInput)) {
          nicknameValidation.textContent = "닉네임은 2자 이상 15자 이하, 영/한/숫자만 가능합니다.";
          nicknameValidation.style.color = "red";
          isNicknameValid = false;
          return;
      } else {
      isNicknameValid = await checkNicknameDuplicate(nicknameInput); // 중복체크 함수 > 서버 호출 || 중복이면 isNicknameValid = false
      }

      // 닉네임 상태 변수 설정( 회원가입 제출시 닉네임란 검증)
      nicknameInputElement.dataset.isValid = isNicknameValid; // 변수 이름 수정
  });


    // 폼 제출 시 이메일 검증 상태 확인
    document.querySelector("form").addEventListener("submit", (event) => {
        const isEmailValid = document.getElementById("email").dataset.isValid === "true"; // 이메일 검증 상태 읽기
        const isPasswordValid = document.getElementById("password").dataset.isValid === "true"; // 비밀번호 검증 상태 읽기
        const isPasswordCheckValid = document.getElementById("password-check").dataset.isValid === "true"; // 비밀번호체크 검증 상태 읽기
        const isNicknameValid = document.getElementById("nickname").dataset.isValid === "true"; // 닉네임 검증 상태 읽기
        const passwordInput = document.getElementById("password").value; // 비밀번호 입력 값
        const passwordValidation = document.getElementById("password-validation"); // 입력란 밑 경고메세지

        const passwordCheckInput = document.getElementById("password-check").value; //비밀번호확인 입력값
        const passwordCheckValidation = document.getElementById("Password-check-validation");  //입력란 밑 경고메세지
        if (!isEmailValid) {
            event.preventDefault(); // 제출 중단
            alert("아이디 중복검사를 진행해 주세요!");
            return;
        }
        if (!isPasswordValid) {
            event.preventDefault(); // 제출 중단
            alert("입력란 경고문을 확인해 주세요!");
            // 비밀번호 필수 항목 체크
            if (passwordInput.trim() === "") { // 입력값이 없으면 실행
                passwordValidation.textContent = "필수 입력란 입니다.";
                passwordValidation.style.color = "red";
                isPasswordValid = false
                return;
            }
            return;
        }
        if (!isPasswordCheckValid) {
            event.preventDefault(); // 제출 중단
            alert("입력란 경고문을 확인해 주세요!");
                if (passwordCheckInput === "") {
                    passwordCheckValidation.textContent = "필수 입력란 입니다.";
                    passwordCheckValidation.style.color = "red";
                    isPasswordCheckValid = false; // 무효 상태로 설정
                    return;
                }
            return;
        }
        if(!isNicknameValid) {
            event.preventDefault(); // 제출 중단
            alert("닉네임 중복검사를 진행해 주세요!");
            return;
        }
    });
});


// 이메일 중복 확인 (서버 호출)
async function checkEmailDuplicate(emailInput) {
    try {
        // 서버에 POST 요청
        const response = await fetch("/api/check-email", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: emailInput }), // 이메일을 JSON 형식으로 서버에 전송
        });

        // 서버 응답이 성공적이지 않으면 오류 발생
        if (!response.ok) {
            throw new Error("Failed to check email duplicate");
        }

        // 응답 JSON 파싱
        const isDuplicate = await response.json();
        const emailValidation = document.getElementById("email-validation");

        let isEmailValid;

        // 중복 여부에 따른 메시지 처리
        if (isDuplicate) {
            emailValidation.textContent = "이미 사용 중인 이메일입니다.";
            emailValidation.style.color = "red";
            isEmailValid = false;
        } else {
            emailValidation.textContent = "사용 가능한 이메일입니다.";
            emailValidation.style.color = "green";
            isEmailValid = true;
        }

        return isEmailValid; // 이메일 유효 여부 반환
    } catch (error) {
        console.error("Error:", error);
        return false; // 오류 발생 시 이메일 유효하지 않음
    }
}



// 닉네임 중복 확인 함수 (서버 호출)
async function checkNicknameDuplicate(nicknameInput) {
    try {
        // 서버에 POST 요청
        const response = await fetch("/api/check-nickname", {
            method: "POST", // POST 방식 지정
            headers: {
                "Content-Type": "application/json", // 요청 본문을 JSON 형식으로 지정
            },
            body: JSON.stringify({ nickname: nicknameInput }), // JSON 형식으로 닉네임 데이터 전송
        });

        // 서버 응답이 성공적이지 않으면 오류 발생
        if (!response.ok) {
            throw new Error("Failed to check nickname duplicate");
        }

        // 응답 JSON 파싱
        const isDuplicate = await response.json();
        const nicknameValidation = document.getElementById("nickname-validation");

        // 중복 여부에 따른 메시지 처리
        if (isDuplicate) {
            nicknameValidation.textContent = "이미 사용 중인 닉네임입니다.";
            nicknameValidation.style.color = "red";
            return false; // 중복된 닉네임이면 유효하지 않음
        } else {
            nicknameValidation.textContent = "사용 가능한 닉네임입니다.";
            nicknameValidation.style.color = "green";
            return true; // 사용 가능한 닉네임이면 유효함
        }
    } catch (error) {
        console.error("Error:", error);
        const nicknameValidation = document.getElementById("nickname-validation");
        nicknameValidation.textContent = "중복 확인 중 오류가 발생했습니다.";
        nicknameValidation.style.color = "red";
        return false; // 오류 발생 시 닉네임 유효하지 않음
    }
}

// 비밀번호 확인 상태를 업데이트하는 함수
function updatePasswordCheckValidation() {
    const passwordInput = document.getElementById("password").value;
    const passwordCheckInput = document.getElementById("password-check").value;
    const passwordCheckValidation = document.getElementById("Password-check-validation");
    const passwordCheckInputElement = document.getElementById("password-check"); // 비밀번호체크 검증 상태 읽기


    if (passwordCheckInput.trim() === "") { // 입력값이 없으면 실행
        passwordCheckValidation.textContent = "";
        passwordCheckInputElement.dataset.isValid = false; // 무효 상태로 설정
    }else if (passwordInput === passwordCheckInput) {
        passwordCheckValidation.textContent = "비밀번호가 일치합니다.";
        passwordCheckValidation.style.color = "green";
        passwordCheckInputElement.dataset.isValid = true; // 유효 상태로 설정
    } else {
        passwordCheckValidation.textContent = "비밀번호가 일치하지 않습니다.";
        passwordCheckValidation.style.color = "red";
        passwordCheckInputElement.dataset.isValid = false; // 무효 상태로 설정
    }
}


