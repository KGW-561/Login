package com.team3.scvs.repository;

import com.team3.scvs.entity.CommunityEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CommunityRepository extends JpaRepository<CommunityEntity, Long> {
    Optional<CommunityEntity> findByTickerId(Long tickerId);
}
