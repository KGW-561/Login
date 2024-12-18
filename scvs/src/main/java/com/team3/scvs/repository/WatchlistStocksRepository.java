package com.team3.scvs.repository;

import com.team3.scvs.entity.TickerEntity;
import com.team3.scvs.entity.UserWatchlistEntity;
import com.team3.scvs.entity.WatchlistStocksEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface WatchlistStocksRepository extends JpaRepository<WatchlistStocksEntity, Long> {

    Optional<WatchlistStocksEntity> findByUserWatchlistUserWatchlistIdAndTickerTickerId(Long userWatchlistId, Long tickerId);

    Optional<WatchlistStocksEntity> findByUserWatchlistAndTicker(UserWatchlistEntity userWatchlist, TickerEntity ticker);

    boolean existsByUserWatchlistAndTicker(UserWatchlistEntity userWatchlist, TickerEntity ticker);
    }
