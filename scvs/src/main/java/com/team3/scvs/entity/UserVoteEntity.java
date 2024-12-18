package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "uservote")
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class UserVoteEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "uservote_id")
    private long uservoteId;

    @Column(name = "user_id")
    private long userId;

    @Column(name = "community_id")
    private long communityId;

    @Column(name = "vote")
    private boolean vote; // 기본값 설정

    @Column(name = "created_at")
    private LocalDateTime createdAt;
}
