package com.team3.scvs.entity;


import jakarta.persistence.*;

import jakarta.persistence.Entity;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "forex") // DB 테이블 이름 forex
@Getter
@Setter
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class ForexEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long forexId; // user_id와 같습니다.

    private String forexName;//지표 이름
    private double rate; // 현재 값
    private double changeValue; // 전날 대비 증감량
    private double changePercent; // 전날 대비 증감율(%)
    private LocalDateTime lastUpdated; // 최신 반영 시간
}
