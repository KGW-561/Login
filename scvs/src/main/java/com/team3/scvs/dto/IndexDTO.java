package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
/**
 * KOSDAQ, KOSPI, NASDAQ, S&P500 지수
 */
public class IndexDTO {
    private String title;
    private double currentValue;
    private double changeValue;
    private double changePercent;
}
