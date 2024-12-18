package com.team3.scvs.dto;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

public class StocksDTO {
    private Long stockId;

    private Long tickerId;

    private String market;
    private BigDecimal currentPrice;
    private BigDecimal close;
    private BigDecimal open;
    private Long volume;
    private BigDecimal fiftytwoWeekLow;
    private BigDecimal fiftytwoWeekHigh;
    private BigDecimal dayLow;
    private BigDecimal dayHigh;
    private BigDecimal returnOnAssets;
    private BigDecimal returnOnEquity;
    private BigDecimal enterpriseValue;

    @Column(name = "enterprise_to_ebitda")
    private BigDecimal enterpriseToEBITDA;

    private BigDecimal priceToBook;
    private BigDecimal priceToSales;
    private BigDecimal earningsPerShare;
    private BigDecimal currentRatio;
    private BigDecimal debtToEquity;
}
