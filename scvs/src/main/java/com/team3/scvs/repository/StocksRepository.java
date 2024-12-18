package com.team3.scvs.repository;

import com.team3.scvs.entity.StocksEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface StocksRepository extends JpaRepository<StocksEntity, Long> {
    Optional<StocksEntity> findByTickerId(Long tickerId);
}
