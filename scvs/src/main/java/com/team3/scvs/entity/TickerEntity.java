package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@Table(name = "tickers")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TickerEntity {

    @Id
    //id 필드가 자동으로 증가된 값으로 설정
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long tickerId;

    private String symbol;

    private String company;
}
