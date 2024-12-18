package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@Data
@Table(name = "community_votes")
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class CommunityVoteEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long communityVoteId;

    // 외래키
    @ManyToOne
    @JoinColumn(name = "community_id", nullable = false)
    private CommunityEntity community;
    @Column(name = "positive_votes")
    private long positiveVotes;
    @Column(name = "negative_votes")
    private long negativeVotes;
}
