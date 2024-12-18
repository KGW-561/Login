package com.team3.scvs.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.team3.scvs.dto.UserDTO;
import com.team3.scvs.service.UserService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
@AutoConfigureMockMvc(addFilters = false) // Security 필터 비활성화
class UserControllerTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    // 회원가입 화면 호출 테스트
    @Test
    void testSignupView() throws Exception {
        // given
        String randomNickname = "TestUser123";
        Mockito.when(userService.generateRandomNickname()).thenReturn(randomNickname);

        mockMvc.perform(get("/signup")) // when
                .andExpect(status().isOk()) // then
                .andExpect(view().name("Account/signup"))
                .andDo(print());


    }

    // 회원가입 기능 테스트
    @Test
    void testSignup() throws Exception {
        // given
        UserDTO userDTO = new UserDTO();
        userDTO.setUserId(1L);
        userDTO.setEmail("test@example.com");
        userDTO.setPassword("StrongPass1!");
        userDTO.setNickname("testUser");
        userDTO.setUserrole("ROLE_USER");

        mockMvc.perform(post("/signup") // when
                        .flashAttr("userDTO", userDTO)) // addAtrtribute 데이터 바인딩
                .andExpect(status().is3xxRedirection()) // then 리다이렉션이 발생하였는가
                .andExpect(redirectedUrl("/signupSuccess")); // 뷰 확인

        Mockito.verify(userService).registerUser(any(UserDTO.class));
    }

    // 이메일 중복 체크 테스트
    @ParameterizedTest
    @CsvSource({
            "test@example.com, true", // 중복 이메일
            "unique@example.com, false" // 비중복 이메일
    })
    void testCheckEmailDuplicate(String email, boolean isDuplicate) throws Exception {
        // given
        Map<String, String> request = Map.of("email", email);
        Mockito.when(userService.isEmailDuplicate((email))).thenReturn(isDuplicate);

        mockMvc.perform(post("/api/check-email") // when
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk()) // then
                .andExpect(content().string(String.valueOf(isDuplicate))); // 예상 결과 검증
    }

    // 닉네임 중복 체크 테스트
    @ParameterizedTest
    @CsvSource({
            "테스트101, true", // 중복닉네임
            "라이언101, false" // 고유 닉네임
    })
    void testCheckNicknameDuplicate(String nickname, boolean isDuplicate) throws Exception {
        // given
        Map<String, String> request = Map.of("nickname", nickname);
        Mockito.when(userService.isNicknameDuplicate((nickname))).thenReturn(isDuplicate);

        mockMvc.perform(post("/api/check-nickname") // when
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk()) // then
                .andExpect(content().string(String.valueOf(isDuplicate)));
    }

    // 비밀번호 중복 체크 테스트
    @ParameterizedTest
    @CsvSource({
            "duplicate123!@, true", // 중복비밀번호
            "uniquePassword123!@, false" // 고유한 비밀번호
    })
    void testCheckPasswordDuplicate(String password, boolean isDuplicate) throws Exception {
        // given
        Map<String, String> request = Map.of("password", password);
        Mockito.when(userService.isPasswordDuplicate(password)).thenReturn(isDuplicate); // Mock 동작 설정

        // when, then
        mockMvc.perform(post("/api/check-password") // when
                        .contentType(MediaType.APPLICATION_JSON) // JSON 요청
                        .content(new ObjectMapper().writeValueAsString(request))) // JSON Body 설정
                .andExpect(status().isOk()) // then HTTP 상태 코드 검증
                .andExpect(content().string(String.valueOf(isDuplicate))); // 응답 본문 검증
    }

    // 사용자 정보 업데이트 테스트
    @Test
    void testUpdateUser() throws Exception {
        // given
        UserDTO userDTO = new UserDTO();
        userDTO.setUserId(1L);
        userDTO.setEmail("test@example.com");
        userDTO.setPassword("StrongPass1!");
        userDTO.setNickname("testUser");
        userDTO.setUserrole("ROLE_USER");

        mockMvc.perform(post("/user/update") //when
                        .flashAttr("userDTO", userDTO))
                .andExpect(status().is3xxRedirection()) // then
                .andExpect(redirectedUrl("/user/profile"));

        Mockito.verify(userService).updateUser(any(UserDTO.class));
    }

    // 회원 탈퇴 테스트
    @Test
    void testDeleteUser() throws Exception {
        mockMvc.perform(post("/user/accountdel")) // when
                .andExpect(status().is3xxRedirection()) // then
                .andExpect(redirectedUrl("/accountdelsuccess"));

        Mockito.verify(userService).deleteUser(any(), any());
    }
}
