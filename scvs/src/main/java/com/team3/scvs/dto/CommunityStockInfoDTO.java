package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CommunityStockInfoDTO {
    private long tickerId;
    private String symbol;
    private String company;
    private String market;
    private long currentPrice;
}

