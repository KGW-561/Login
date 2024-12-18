package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.Immutable;

import java.time.LocalDateTime;

@Entity
@Data
@Immutable
@Table(name = "vw_user_comments")
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class CommunityCommentViewEntity {

    @Id
    @Column(name = "community_comment_id")
    private Long id;

    @Column(name = "user_id")
    private long userId;

    @Column(name = "community_id")
    private long communityId;

    @Column(name = "nickname")
    private String nickname;

    @Column(nullable = false, length = 255)
    private String comment;

    @Column(name = "published_at")
    private LocalDateTime publishedAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    @Column(name = "time_ago")
    private String timeAgo;
}
