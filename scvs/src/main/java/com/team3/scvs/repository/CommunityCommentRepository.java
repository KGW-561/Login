package com.team3.scvs.repository;

import com.team3.scvs.entity.CommunityCommentEntity;
import org.springframework.data.jpa.repository.JpaRepository;


public interface CommunityCommentRepository extends JpaRepository<CommunityCommentEntity, Long> {
}
