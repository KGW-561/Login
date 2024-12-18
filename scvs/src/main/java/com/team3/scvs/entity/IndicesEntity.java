package com.team3.scvs.entity;


import jakarta.persistence.Entity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "indices") // DB 테이블 이름 indices
@Getter
@Setter
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class IndicesEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long indexId; // user_id와 같습니다.

    private String title;//지표 이름
    private double currentValue; // 현재 값
    private double changeValue; // 전날 대비 증감량
    private double changePercent; // 전날 대비 증감율(%)
}
