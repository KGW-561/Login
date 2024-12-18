package com.team3.scvs.entity;


import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@Data
@Table(name = "community")
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class CommunityEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long communityId;

    // 외래키
    @Column(name = "ticker_id")
    private long tickerId;
}

