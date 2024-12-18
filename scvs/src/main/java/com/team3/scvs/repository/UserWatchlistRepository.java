package com.team3.scvs.repository;

import com.team3.scvs.entity.UserWatchlistEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface UserWatchlistRepository extends JpaRepository<UserWatchlistEntity, Long> {

    // 특정 사용자 ID로 관심 목록 조회
    List<UserWatchlistEntity> findByUserId(Long userId);

    // 관심 목록 존재 여부 확인
    boolean existsById(Long watchlistId);

}
