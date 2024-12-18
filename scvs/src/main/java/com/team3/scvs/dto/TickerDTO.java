package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class TickerDTO {
    private Long tickerId;  // 종목 ID
    private String symbol;  // 주식 심볼
    private String company; // 회사 이름
}
