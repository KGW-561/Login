package com.team3.scvs.repository;

import com.team3.scvs.entity.CommunityCommentViewEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface CommunityCommentViewRepository extends JpaRepository<CommunityCommentViewEntity, Long> {

    @Query("SELECT c FROM CommunityCommentViewEntity c WHERE c.communityId = :communityId ORDER BY c.publishedAt DESC")
    List<CommunityCommentViewEntity> findAllByCommunityIdOrderByPublishedAtDesc(@Param("communityId") Long communityId);

    // 특정 communityId에 대한 최신 댓글 가져오기
    Optional<CommunityCommentViewEntity> findTopByCommunityIdOrderByPublishedAtDesc(long communityId);

    // 특정 communityId에 대한 댓글 수 가져오기
    long countByCommunityId(long communityId);
}

