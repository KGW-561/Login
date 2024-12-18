package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
/*
원/달러 환율 지수
 */
public class ForexDTO {
    private String forexName;
    private double rate;
    private double changeValue;
    private double changePercent;
    private LocalDateTime lastUpdated;
}
