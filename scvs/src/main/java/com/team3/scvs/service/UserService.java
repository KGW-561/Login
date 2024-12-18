package com.team3.scvs.service;

import com.team3.scvs.constant.UserConstants;
import com.team3.scvs.dto.UserDTO;
import com.team3.scvs.entity.UserEntity;
import com.team3.scvs.repository.UserRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.AuthenticationCredentialsNotFoundException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.stereotype.Service;

import java.util.Random;


@Service
public class UserService {


    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    // 생성자 주입
    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    // 난수 생성
    private final Random random = new Random();

    // 회원가입에 사용
    // 닉네임 랜덤생성 앞단어 + 뒷단어 + 난수(1~1000)으로 생성 ex)맑은나무444
    public String generateRandomNickname() {
        String randomNickname; // 랜덤 닉네임 변수
        int attempts = 0;

        do {

            String firstPart = UserConstants.FIRST_PARTS[random.nextInt(UserConstants.FIRST_PARTS.length)];
            String secondPart = UserConstants.SECOND_PARTS[random.nextInt(UserConstants.SECOND_PARTS.length)];
            int randomNumber = this.random.nextInt(1000) + 1; // 1~1000 난수
            attempts++; // 시도 1회 증가

            if (attempts >= UserConstants.MAX_ATTEMPTS) { // 시도가 100회이상이 되면
                throw new IllegalArgumentException("닉네임 생성 실패: 중복을 피할 수 없습니다."); // 에러발생
            }
            randomNickname = firstPart + secondPart + randomNumber;
        } while (isNicknameDuplicate(randomNickname)); // DB에서 중복된 닉네임이 있으면 true 반복


        return randomNickname;
    }

    // 이메일 중복확인, 회원가입 정보수정에 사용
    public boolean isEmailDuplicate(String email) {
        return userRepository.existsByEmail(email);
    }
    // 닉네임 중복확인, 회원가입 정보수정에 사용
    public boolean isNicknameDuplicate(String nickname) {
        return userRepository.existsByNickname(nickname);
    }
    // 패스워드 중복확인, 비밀번호 수정에 사용
    public boolean isPasswordDuplicate(String password) {

        String username = getAuthenticatedUsername(); // 가져온 username변수

        // DB에서 username으로 조회
        UserEntity userEntity = userRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException(UserConstants.USER_NOT_FOUND_ERROR + username)); // 예시로 이메일을 사용
        // 사용자가 입력한 비밀번호와 DB에서 가져온 암호화된 비밀번호 비교
        return passwordEncoder.matches(password, userEntity.getPassword());
    }


    // Create(회원가입)
    public void registerUser(UserDTO userDTO) {
        if (userDTO == null) {
            throw new IllegalArgumentException("UserDTO cannot be null.");
        }

        // UserDTO에서 UserEntity로 저장 > DB에 저장
        UserEntity userEntity = new UserEntity();
        userEntity.setEmail(userDTO.getEmail());
        userEntity.setPassword(passwordEncoder.encode(userDTO.getPassword())); // 비밀번호 암호화
        userEntity.setNickname(userDTO.getNickname());
        userEntity.setUserrole("ROLE_USER");

        userRepository.save(userEntity); // db저장 실행
    }

    // Read(User ReadDB에서 값을 가져와 UserDTO를 리턴 (로그인에서는 사용하지 않음))
    public UserDTO getUser(){

        // 현재 로그인된 email를 저장
        String username = getAuthenticatedUsername();

        // DB에서 username으로 조회
        UserEntity userEntity = userRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException(UserConstants.USER_NOT_FOUND_ERROR + username)); // 로그인상태여서 DB에 값이 없으면 안됨 > 오류 발생

        UserDTO userDTO = new UserDTO();
        setDtoFromEntity(userDTO, userEntity); // DB 에서 가져온 UserEntity를 UserDTO에 매칭

        return userDTO;
    }

    // DB에서 가져온 UserEntity값을 UserDTO에 설정한다.
    public void setDtoFromEntity(UserDTO userDTO , UserEntity userEntity){
        userDTO.setEmail(userEntity.getEmail());
        userDTO.setNickname(userEntity.getNickname());
        userDTO.setUserrole(userEntity.getUserrole());
    }

    // Update(회원정보 수정, 세션업데이트)
    public void updateUser(UserDTO userDTO) {
        // 현재 로그인된 email를 저장
        String username = getAuthenticatedUsername(); // 가져온 username변수

        // DB에서 UserEntity를 가져옴
        UserEntity user = userRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException(UserConstants.USER_NOT_FOUND_ERROR + username));

        // null이 아니면 email 수정
        if (userDTO.getEmail() != null) {
            user.setEmail(userDTO.getEmail());
        }

        // null이 아니면 nickname 수정
        if (userDTO.getNickname() != null) {
            user.setNickname(userDTO.getNickname());
        }

        // null이 아니면 password 수정
        if (userDTO.getPassword() != null) {
            user.setPassword(passwordEncoder.encode(userDTO.getPassword()));
        }
        // SecurityContext에 업데이트( 현재 로그인정보수정)
        updateSecurityContext(user);

        // DB에 업데이트된 정보 저장
        userRepository.save(user);


    }

    // Delete (회원정보 삭제)
    public void deleteUser(HttpServletRequest request, HttpServletResponse response) {
        // 현재 로그인된 정보를 가져옴
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = auth.getName(); // 가져온 username변수

        // DB에서 UserEntity를 가져옴
        UserEntity user = userRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException(UserConstants.USER_NOT_FOUND_ERROR + username));

        new SecurityContextLogoutHandler().logout(request, response, auth);

        // DB에 해당 user데이터 삭제
        userRepository.delete(user);
    }

    // SecurityContext를 업데이트하는 메서드
    private void updateSecurityContext(UserEntity userEntity) {
        Authentication currentAuth = SecurityContextHolder.getContext().getAuthentication();
        // 새로운 UserDetails 생성
        UserDetails updatedUserDetails = new User(
                userEntity.getEmail(),          // 수정된 email
                userEntity.getPassword(),       // 수정된 password
                currentAuth.getAuthorities()    // 기존 권한
        );

        // 새로운 인증 토큰 생성
        Authentication newAuth = new UsernamePasswordAuthenticationToken(
                updatedUserDetails,
                currentAuth.getCredentials(),
                updatedUserDetails.getAuthorities()
        );

        // SecurityContext에 새 인증 정보 설정
        SecurityContextHolder.getContext().setAuthentication(newAuth);
    }

    // 세션에 저장된 SecurityContext에서 인증된 사용자의 Username을 리턴
    public String getAuthenticatedUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null) {
            throw new AuthenticationCredentialsNotFoundException("사용자가 인증되지 않았습니다.");
        }
        return auth.getName();
    }

    public Long getUserId(String userName){
        UserEntity userEntity = userRepository.findByEmail(userName).orElse(null);
        if(userEntity == null){
            return -1L;
        }
        return userEntity.getUserId();
    }
}
