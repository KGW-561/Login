package com.team3.scvs.entity;


import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "users") // DB 테이블 이름 users
@Getter
@Setter
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class UserEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long userId; // user_id와 같습니다.


    private String email; // 이메일
    private String password; // 암호화된 비밀번호
    private String nickname; // 닉네임
    private String userrole; // 역할 user or admin
}
