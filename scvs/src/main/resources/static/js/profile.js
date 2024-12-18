document.addEventListener("DOMContentLoaded", () => {

    //  내정보에 불러드린 값은 valid값이 true
    document.getElementById("email").dataset.isValid = true;
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
        const originalEmail = document.getElementById("current-email").textContent;
        const emailInput = document.getElementById("email").value; // 이메일 입력 값
        const emailValidation = document.getElementById("email-validation"); // 입력란 밑 경고메세지
        const emailInputElement = document.getElementById("email");     // email을 받아옴 나중에 제출할때 검증할때 사용
        let isEmailValid = false; // 이메일 검증 상태 변수

        // 수정하지 않은 경우 처리
        if (originalEmail === emailInput) {
            document.getElementById("email-validation").textContent = "현재 이메일과 동일합니다. 중복 확인이 필요 없습니다.";
            emailValidation.style.color = "green";
            isEmailValid = true;
            emailInputElement.dataset.isValid = isEmailValid;
            return;
        }
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
        // 이메일 상태 변수 설정( 정보수정 제출시 이메일란 검증)
        emailInputElement.dataset.isValid = isEmailValid;
    });

     // 닉네임 중복 확인 버튼 이벤트 리스너
      document.getElementById("check-nickname-duplicate").addEventListener("click", async () => {
          const originalNickname = document.getElementById("current-nickname").textContent;
          const nicknameInput = document.getElementById("nickname").value; // 닉네임 입력값
          const nicknameValidation = document.getElementById("nickname-validation"); //입력란 밑 경고메세지
          const nicknameInputElement = document.getElementById("nickname");     // nickname을 받아옴 나중에 제출할때 검증할때 사용
          let isNicknameValid = false; // 이메일 검증 상태 변수


          // 수정하지 않은 경우 처리
          if (originalNickname === nicknameInput) {
              document.getElementById("nickname-validation").textContent = "현재 닉네임과 동일합니다. 중복 확인이 필요 없습니다.";
              nicknameValidation.style.color = "green";
              isNicknameValid = true;
              return;
          }

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

          // 닉네임 상태 변수 설정( 정보수정 제출시 닉네임란 검증)
          nicknameInputElement.dataset.isValid = isNicknameValid; // 변수 이름 수정
      });

      // 폼 제출 시 이메일 검증 상태 확인
      document.querySelector("form").addEventListener("submit", (event) => {
          const isEmailValid = document.getElementById("email").dataset.isValid === "true"; // 이메일 검증 상태 읽기
          const isNicknameValid = document.getElementById("nickname").dataset.isValid === "true"; // 닉네임 검증 상태 읽기

          if (!isEmailValid) {
              event.preventDefault(); // 제출 중단
              alert("아이디 중복검사를 진행해 주세요!");
              return;
          }
          if(!isNicknameValid) {
              event.preventDefault(); // 제출 중단
              alert("닉네임 중복검사를 진행해 주세요!");
              return;
          }

          // 확인 창 띄우기
          const isConfirmed = confirm("회원정보를 수정하시겠습니까?");
          if (!isConfirmed) {
              // "취소"를 누르면 폼 제출 중단
              event.preventDefault();
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