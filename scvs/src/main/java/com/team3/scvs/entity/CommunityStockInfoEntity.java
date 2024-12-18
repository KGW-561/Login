package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;
import org.hibernate.annotations.Immutable;

@Entity
@Data
@Immutable //읽기전용 Entity
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
@Table(name = "vw_community_stockinfo")
public class CommunityStockInfoEntity {

    @Id
    @Column(name = "ticker_id")
    private long tickerId;

    private String symbol;
    private String company;
    private String market;

    @Column(name = "current_price")
    private long currentprice;
}

