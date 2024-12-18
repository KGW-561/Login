package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@Table(name = "watchlist_stocks")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class WatchlistStocksEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long watchlistStockId;
    //N:1관계 지연 로딩 방식(효율성과 자원절약을 하기위해 fetch = FetchType.Lazy를 사용)
    @ManyToOne(fetch = FetchType.LAZY)
    //외래키
    @JoinColumn(name = "watchlist_id", nullable = false)
    private UserWatchlistEntity userWatchlist;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticker_id", nullable = false)
    private TickerEntity ticker;
}
