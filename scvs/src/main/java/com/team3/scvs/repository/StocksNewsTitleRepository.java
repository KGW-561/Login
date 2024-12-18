package com.team3.scvs.repository;

import com.team3.scvs.entity.StockNewsTitleEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StocksNewsTitleRepository extends JpaRepository<StockNewsTitleEntity, String> {

    @Query("SELECT s FROM StockNewsTitleEntity s WHERE s.tickerId = :tickerId ORDER BY s.publishedAt DESC")
    List<StockNewsTitleEntity> findLatestByTickerId(@Param("tickerId") long tickerId);

}
