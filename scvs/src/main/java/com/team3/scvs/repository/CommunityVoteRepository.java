package com.team3.scvs.repository;

import com.team3.scvs.entity.CommunityVoteEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CommunityVoteRepository extends JpaRepository<CommunityVoteEntity, Long> {
    Optional<CommunityVoteEntity> findByCommunity_CommunityId(Long communityId);
}
