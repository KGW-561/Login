package com.team3.scvs.repository;


import com.team3.scvs.entity.UserEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<UserEntity, Long> {

    boolean existsByEmail(String email);    // 이메일유무(중복확인에 사용) 중복이면 true
    boolean existsByNickname(String nickname); // 닉네임유무(중복확인에 사용) 중복이면 true


    Optional<UserEntity> findByEmail(String email); // UserEntity반환(로그인에 사용)


    Page<UserEntity> findByEmailContaining(String input, Pageable pageable); // 관리자가 이메일로 유저 검색
    Page<UserEntity> findByNicknameContaining(String input, Pageable pageable); // 관리자가 닉네임으로 유저 검색
}
