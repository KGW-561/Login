package com.team3.scvs.repository;

import com.team3.scvs.entity.StockNewsEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;


public interface StockNewsRepository extends JpaRepository<StockNewsEntity, String> {

    Page<StockNewsEntity> findByTickerId(Long tickerId, Pageable pageable);

}
