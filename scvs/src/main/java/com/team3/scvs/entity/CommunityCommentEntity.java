package com.team3.scvs.entity;


import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "community_comments")
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class CommunityCommentEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long communityCommentId;

    //외래키
    @ManyToOne
    @JoinColumn(name = "community_id", nullable = false)
    private CommunityEntity community;

    //외래키
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @Column(nullable = false, length = 255)
    private String comment;
    @Column(name = "published_at")
    private LocalDateTime publishedAt;
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // 생성 시 publishedAt 설정
    @PrePersist
    protected void onCreate() {
        this.publishedAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    // 수정 시 updatedAt 설정
    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

}
