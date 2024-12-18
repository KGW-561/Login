package com.team3.scvs.controller;

import com.team3.scvs.dto.UserDTO;
import com.team3.scvs.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.Map;

@Slf4j
@Controller
public class UserController {


    private final UserService userService;
    // 생성자 주입
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/login")
    public String loginPage(Model model) {
        return "Account/login";
    }

    // 회원가입 화면 호출
    @GetMapping("/signup")
    public String signupView(Model model) {
        // 랜덤 닉네임생성 and UserDTO전달
        UserDTO userDTO = new UserDTO();
        String randomNickname = userService.generateRandomNickname(); // 랜덤 닉네임 생성
        userDTO.setNickname(randomNickname);    // 닉네임 초기값 세팅
        model.addAttribute("userDTO", userDTO); // 회원

        return "Account/signup";
    }
    // 회원가입 기능
    @PostMapping("/signup")
    public String signup(UserDTO userDTO) {
        userService.registerUser(userDTO); // 회원가입서비스 호출
        return "redirect:/signupSuccess";
    }
    // 성공화면 호출
    @GetMapping("/signupSuccess")
    public String showLoginSuccessPage() {
        return "Account/signupSuccess";  // signupSuccess.html을 반환
    }


    // 이메일 중복체크 api
    @PostMapping("/api/check-email")
    public ResponseEntity<Boolean> checkEmailDuplicate(@RequestBody Map<String, String> request) {
        String email = request.get("email"); // 클라이언트에서 전송한 이메일
        boolean isDuplicate = userService.isEmailDuplicate(email);
        return ResponseEntity.ok(isDuplicate);
    }
    // 닉네임 중복체크 api
    @PostMapping("/api/check-nickname")
    public ResponseEntity<Boolean> checkNicknameDuplicate(@RequestBody Map<String, String> request) {
        String nickname = request.get("nickname"); // 클라이언트에서 전송한 닉네임
        boolean isDuplicate = userService.isNicknameDuplicate(nickname);
        return ResponseEntity.ok(isDuplicate);
    }
    // 비밀번호 중복체크 api
    @PostMapping("/api/check-password")
    public ResponseEntity<Boolean> checkPasswordDuplicate(@RequestBody Map<String, String> request) {
        String password = request.get("password"); // 클라이언트에서 전송한 패스워드
        boolean isDuplicate = userService.isPasswordDuplicate(password);
        return ResponseEntity.ok(isDuplicate);
    }

    // 내정보 화면 호출
    @GetMapping("/user/profile")
    public String showProfilePagePage(Model model){
        model.addAttribute(userService.getUser());
        return "User/profile";
    }
    // 내정보수정 - 유저정보 업데이트
    @PostMapping("/user/update")
    public String updateUser(UserDTO userDTO){
        userService.updateUser(userDTO);
        return "redirect:/user/profile";
    }
    // 비밀번호 확인 화면 호출
    @GetMapping("/user/passwordcheck")
    public String showPasswordCheckPage(){
        return "User/passwordcheck";
    }
    // 비밀번호 수정 화면 호출
    @GetMapping("/user/passwordchange")
    public String showPasswordChangePage(Model model){
        model.addAttribute(userService.getUser());  // userDTO로 주고 받음
        return "User/passwordchange";
    }
    // 회원 탈퇴 화면 호출
    @GetMapping("/user/accountdel")
    public String showAccountDelPage(){
        return "User/accountdel";
    }
    // 회원 탈퇴 기능
    @PostMapping("/user/accountdel")
    public String deleteUser(HttpServletRequest request, HttpServletResponse response){
        userService.deleteUser(request, response);
        return "redirect:/accountdelsuccess";
    }
    // 회원탈퇴 뷰 호출
    @GetMapping("/accountdelsuccess")
    public String showAccountDelSuccessPage() {
        return "User/accountdelsuccess";  // accountdelsuccess.html을 반환
    }

}
