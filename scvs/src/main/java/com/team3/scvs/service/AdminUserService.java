package com.team3.scvs.service;

import com.team3.scvs.dto.UserDTO;
import com.team3.scvs.entity.UserEntity;
import com.team3.scvs.repository.UserRepository;
import com.team3.scvs.util.ConvertUtil;
import groovy.util.logging.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

@Slf4j
@Service
public class AdminUserService {
    private static final Logger log = LoggerFactory.getLogger(AdminUserService.class);
    private final UserRepository userRepository;
    // 생성자 주입
    public AdminUserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // 필터에 따른 검색
    public Page<UserDTO> getFilteredUsers(String filter, String input, Pageable pageable) {
        // 입력값이 공백만 있는 경우 오류 처리
        if (input != null && input.trim().isEmpty()) {
            return getUsers(pageable);
        }
        if ("email".equals(filter)) {
            return userRepository.findByEmailContaining(input, pageable).map(ConvertUtil::convertToDTO); // 이메일 필터
        } else if ("nickname".equals(filter)) {
            return userRepository.findByNicknameContaining(input, pageable).map(ConvertUtil::convertToDTO); // 닉네임 필터
        } else {
            return getUsers(pageable); // 필터가 없으면 모든 리스트 반환
        }
    }

    // 필터없이 모든 유저 검색
    public Page<UserDTO> getUsers(Pageable pageable) {
        Page<UserEntity> userEntities = userRepository.findAll(pageable);
        return userEntities.map(ConvertUtil::convertToDTO);
    }

    // 체크리스트를 통한 유저 삭제
    public void deleteUsers(List<Long> userIds) {
        for(Long userId : userIds){
            userRepository.deleteById(userId);
        }
    }
}
