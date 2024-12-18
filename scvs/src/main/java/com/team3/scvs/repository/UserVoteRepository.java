package com.team3.scvs.repository;

import com.team3.scvs.entity.UserVoteEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserVoteRepository extends JpaRepository<UserVoteEntity, Long> {
    Optional<UserVoteEntity> findByUserIdAndCommunityId(Long userId, Long communityId);
}
