package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WatchlistStocksDTO {
    private Long watchlistStockId; // 관심 종목 ID
    private Long watchlistId;      // 관심 목록 ID
    private Long tickerId;         // 종목 ID
}
