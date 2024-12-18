package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "user_watchlist")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserWatchlistEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long userWatchlistId;

    private Long userId;
    //UserWatchlistEntity가 여러 개의 WatchlistStocksEntity와 관계를 맺음
    //데이터베이스에서의 자동적인 관계 처리를 쉽게 하기 위해 cascade와 orphanRemoval 옵션을 추가
    @OneToMany(mappedBy = "userWatchlist", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<WatchlistStocksEntity> stocks;
}
