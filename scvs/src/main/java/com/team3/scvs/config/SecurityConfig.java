package com.team3.scvs.config;


import com.team3.scvs.security.CustomAuthenticationFailureHandler;
import com.team3.scvs.security.CustomAuthenticationSuccessHandler;
import com.team3.scvs.service.CustomUserDetailsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;

@Slf4j
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {


    private final CustomUserDetailsService customUserDetailsService;

    // 암호화
    @Bean
    public BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    // 로그인성공시 실행되는 핸들러 설정
    @Bean
    public AuthenticationSuccessHandler authenticationSuccessHandler() {
        return new CustomAuthenticationSuccessHandler();
    }

    // 로그인실패시 실행되는 핸들러 설정
    @Bean
    public AuthenticationFailureHandler authenticationFailureHandler() {
        return new CustomAuthenticationFailureHandler();
    }

    // 필터에서 Security기본설정 ( 접근권한 , 로그인설정 , 로그아웃설정)
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                    .requestMatchers("/").permitAll() // index 페이지 접근을 인증 없이 허용
                    .requestMatchers("/profile").authenticated() // profile 페이지는 인증된 사용자만 접근
                    .requestMatchers("/admin/**").hasRole("ADMIN") // /admin/**는 ROLE_ADMIN만 접근 가능
                    .anyRequest().permitAll() // 모든 요청은 인증 불필요
            )
            .formLogin(form -> form
                .loginPage("/login") // 로그인 페이지 URL
                .loginProcessingUrl("/login") // 로그인 요청 처리 URL
                .successHandler(authenticationSuccessHandler()) // 커스텀 성공 핸들러
                .failureHandler(authenticationFailureHandler()) // 커스텀 실패 핸들러
                .usernameParameter("email") // 클라이언트의 userDTO.email를 username(Security 로그인 변수)으로 변경
            )
            .logout(form -> form
                .logoutUrl("/logout")   // 로그아웃 페이지 URL
                .logoutSuccessUrl("/") // 로그아웃 성공 시 리다이렉트
            );
        return http.build();
    }

    // Security의 빌더에 사용하는 Service, passwordEncoding를 수정한 메서드로 사용
    @Bean
    public AuthenticationManager authenticationManager(HttpSecurity http) throws Exception {
        // AuthenticationManagerBuilder를 사용하여 AuthenticationManager를 빌드
        AuthenticationManagerBuilder authenticationManagerBuilder = http.getSharedObject(AuthenticationManagerBuilder.class);
        authenticationManagerBuilder
                .userDetailsService(customUserDetailsService) // CustomUserDetailsService 설정
                .passwordEncoder(passwordEncoder()); // PasswordEncoder 설정

        return authenticationManagerBuilder.build(); // AuthenticationManager 객체 반환
    }



}
